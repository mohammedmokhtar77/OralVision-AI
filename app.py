import os
import uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
from utils.predict import OralDiseaseClassifier

app = Flask(__name__)
# Secure session key
app.secret_key = 'ai_oral_disease_detection_secret_key_change_in_prod'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # Strict 10 MB limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Instantiate and load model once when Flask starts
classifier = OralDiseaseClassifier()
try:
    classifier.load_model()
except Exception as e:
    print(f"CRITICAL ERROR loading model: {e}")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_old_uploads():
    """Delete files in the upload directory older than 15 minutes to preserve storage."""
    import time
    now = time.time()
    try:
        for f in os.listdir(app.config['UPLOAD_FOLDER']):
            fp = os.path.join(app.config['UPLOAD_FOLDER'], f)
            if os.path.isfile(fp) and f != '.gitkeep':
                if os.stat(fp).st_mtime < now - 900:  # 15 minutes
                    try:
                        os.remove(fp)
                    except OSError:
                        pass
    except Exception as e:
        print(f"Error executing upload cleanup: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Run directory maintenance
    cleanup_old_uploads()

    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400
        
    if file and allowed_file(file.filename):
        # Generate random unique filename to prevent caching issues
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(filepath)
        
        try:
            # Predict using classifier
            result = classifier.predict(filepath)
            
            # Save results to session
            session['prediction_result'] = {
                'prediction': result['prediction'],
                'class_name': result['class_name'],
                'confidence': result['confidence'],
                'top_predictions': result['top_predictions'],
                'description': result['description'],
                'symptoms': result['symptoms'],
                'recommendation': result['recommendation'],
                'prediction_time': result['prediction_time'],
                'filename': unique_filename
            }
            
            return jsonify({'success': True, 'redirect_url': url_for('result')})
            
        except Exception as e:
            # Delete file if prediction fails
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except OSError:
                    pass
            return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Unsupported file format. Only JPG, JPEG, and PNG images are accepted.'}), 400

@app.route('/result')
def result():
    if request.args.get('new') == 'true':
        session.pop('prediction_result', None)
        return render_template('prediction.html')
        
    prediction_data = session.get('prediction_result')
    if not prediction_data:
        # Re-route to upload page if no prediction in session (Requirement: /result Display prediction page)
        return render_template('prediction.html')
        
    # Verify the image still exists on disk before display
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], prediction_data['filename'])
    if not os.path.exists(filepath):
        session.pop('prediction_result', None)
        return render_template('prediction.html')
        
    return render_template('result.html', data=prediction_data)

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'Uploaded file is too large. Maximum size allowed is 10MB.'}), 413

if __name__ == '__main__':
    # Running app on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
