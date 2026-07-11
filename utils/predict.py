import os
import time
import numpy as np
from PIL import Image
import tensorflow as tf

class OralDiseaseClassifier:
    def __init__(self):
        self.model = None
        # Class index mapping from the training notebook generator
        self.classes = {
            0: "Calculus",
            1: "Caries",
            2: "Gingivitis",
            3: "Hypodontia",
            4: "Mouth Ulcer",
            5: "Tooth Discoloration"
        }
        
        # Clinical metadata for the supported conditions
        self.disease_metadata = {
            "Calculus": {
                "display_name": "Calculus",
                "description": "Hardened dental plaque that forms on teeth when mineral deposits from saliva accumulate. It provides a rough surface that attracts more bacterial plaque, potentially leading to more severe periodontal diseases.",
                "symptoms": [
                    "Hard yellow, brown, or black mineral deposits visible near the gum line",
                    "Red, swollen, or bleeding gums (signs of gingivitis)",
                    "Persistent bad breath (halitosis) that does not improve after brushing"
                ],
                "recommendation": "Professional scaling and polishing by a registered dental hygienist or dentist is required to safely remove tartar. Maintain rigorous oral hygiene with twice-daily brushing using fluoride toothpaste, and practice daily flossing to prevent future build-up."
            },
            "Caries": {
                "display_name": "Caries (Tooth Decay)",
                "description": "Damage to a tooth's enamel and dentin caused by acid-producing bacteria present in dental plaque. If left untreated, cavities can grow larger and affect deeper layers of the tooth.",
                "symptoms": [
                    "Spontaneous toothache or sharp pain when eating/drinking sweet, hot, or cold items",
                    "Visible pits, holes, or structural cavities in the tooth surface",
                    "Dark brown, black, or chalky white staining on any tooth surface"
                ],
                "recommendation": "Consult a dentist immediately for a professional evaluation. Early-stage decay can be treated with topical fluoride, while advanced decay may require dental fillings, crowns, or root canal therapy depending on the pulp's health."
            },
            "Gingivitis": {
                "display_name": "Gingivitis",
                "description": "The earliest and mildest form of periodontal (gum) disease, characterized by inflammation of the gums surrounding the base of your teeth. It is reversible with proper care.",
                "symptoms": [
                    "Gums that are swollen, puffy, or unusually tender to the touch",
                    "Gums that bleed easily, especially during brushing or flossing",
                    "Bad breath and gums that look bright red or dusky red rather than healthy pink"
                ],
                "recommendation": "Improve daily plaque removal by brushing twice daily with a soft-bristled toothbrush and flossing daily. Incorporate an antiseptic mouthwash. Schedule a professional cleaning to remove plaque, and seek dental guidance to prevent progression to periodontitis."
            },
            "Hypodontia": {
                "display_name": "Hypodontia",
                "description": "A developmental anomaly characterized by the congenital absence of one or more teeth, excluding the third molars (wisdom teeth). It can affect both primary and permanent teeth.",
                "symptoms": [
                    "Noticeable spaces or gaps between teeth where permanent teeth failed to erupt",
                    "Difficulty in chewing, biting, or pronouncing certain sounds properly",
                    "Aesthetic concerns or self-consciousness about teeth alignment"
                ],
                "recommendation": "Consult an orthodontist or prosthodontist to establish a treatment plan. Common interventions include orthodontic braces to close spaces or align teeth, space maintainers, dental implants, bridges, or partial dentures to restore oral function and aesthetics."
            },
            "Mouth Ulcer": {
                "display_name": "Mouth Ulcer (Canker Sores)",
                "description": "Small, painful, non-contagious lesions that develop on the soft tissues inside your mouth or at the base of your gums. They typically heal on their own within 10 to 14 days.",
                "symptoms": [
                    "Painful round or oval sores inside the cheeks, lips, or on/under the tongue",
                    "Sores exhibiting a red border with a white, gray, or yellow center",
                    "Increased discomfort or stinging pain while eating spicy, salty, or acidic foods"
                ],
                "recommendation": "Avoid spicy, salty, or acidic foods that can irritate the sores. Use a soft toothbrush and avoid abrasive toothpaste. Apply over-the-counter topical anesthetic gels to soothe pain, or rinse with warm salt water. See a doctor or dentist if the ulcer lasts more than two weeks."
            },
            "Tooth Discoloration": {
                "display_name": "Tooth Discoloration",
                "description": "Staining or changes in the color of teeth. It can be extrinsic (surface staining caused by coffee, tea, red wine, dark sodas, and tobacco) or intrinsic (internal yellowing or staining due to trauma, medication, or aging).",
                "symptoms": [
                    "Yellow, brown, gray, or white spots and streaks on the tooth surfaces",
                    "General dullness or loss of natural tooth enamel luster"
                ],
                "recommendation": "Consult a dentist to determine if the discoloration is surface-based or structural. Treatments can range from professional dental scaling and whitening to cosmetic bonding or porcelain veneers. Limit consumption of teeth-staining food/drinks and brush shortly after."
            }
        }
        
    def load_model(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Check official model path
        model_path = os.path.join(base_dir, 'models', 'best_efficientnet.keras')
        if not os.path.exists(model_path):
            # Check fallback path
            fallback_path = os.path.join(base_dir, 'models', 'EfficientNetModel.keras')
            if os.path.exists(fallback_path):
                model_path = fallback_path
            else:
                raise FileNotFoundError(f"Model file not found. Please place best_efficientnet.keras inside: {os.path.join(base_dir, 'models')}")
        
        print(f"Loading model from: {model_path}")
        self.model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully!")
        
    def predict(self, image_path):
        if self.model is None:
            self.load_model()
            
        start_time = time.time()
        
        # Load and preprocess the image
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
        
        # Convert to numpy array and prepare for model input
        img_array = np.array(img, dtype=np.float32)
        
        # The training notebook uses: preprocessing_function=preprocess_input (where preprocess_input for EfficientNet is a pass-through)
        # Therefore, we keep pixel values in range [0, 255] and expand batch dimensions.
        img_array = np.expand_dims(img_array, axis=0)
        
        # Run inference in silent mode to avoid console logging spam
        predictions = self.model.predict(img_array, verbose=0)[0]
        
        # Sort predictions by confidence desc
        sorted_indices = np.argsort(predictions)[::-1]
        
        top_predictions = []
        for rank, idx in enumerate(sorted_indices):
            class_name = self.classes[idx]
            display_name = self.disease_metadata[class_name]["display_name"]
            confidence = float(predictions[idx]) * 100
            top_predictions.append({
                "rank": rank + 1,
                "class_name": class_name,
                "display_name": display_name,
                "confidence": round(confidence, 2)
            })
            
        primary_pred = top_predictions[0]
        primary_class = primary_pred["class_name"]
        primary_metadata = self.disease_metadata[primary_class]
        
        elapsed_time = (time.time() - start_time) * 1000 # in milliseconds
        
        result = {
            "prediction": primary_pred["display_name"],
            "class_name": primary_class,
            "confidence": f"{primary_pred['confidence']:.2f}%",
            "top_predictions": top_predictions[:3],
            "description": primary_metadata["description"],
            "symptoms": primary_metadata["symptoms"],
            "recommendation": primary_metadata["recommendation"],
            "prediction_time": f"{elapsed_time:.2f} ms"
        }
        
        return result
