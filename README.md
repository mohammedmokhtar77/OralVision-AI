# 🦷 OralVision AI – Oral Disease Detection System

## 📌 Project Overview

OralVision AI is an end-to-end Deep Learning web application for automated oral disease classification from dental images.

The project covers the complete AI workflow, including data preprocessing, exploratory data analysis (EDA), image augmentation, model development, transfer learning, model evaluation, and deployment using Flask.

Four different deep learning architectures were developed and compared to identify the best-performing model for deployment.

The final deployed model is **EfficientNetB0**, which achieved the highest validation performance while maintaining a lightweight architecture suitable for real-time inference.

---

# 📂 Project Workflow

## 1️⃣ Data Collection

- Oral Diseases Image Dataset
- 5,563 labeled RGB images
- 6 oral disease categories

### Classes

- Calculus
- Caries
- Gingivitis
- Hypodontia
- Mouth Ulcer
- Tooth Discoloration

Dataset Split

- Training: **3,894**
- Validation: **834**
- Testing: **835**

---

## 2️⃣ Data Preprocessing

Performed comprehensive image preprocessing including:

- Image resizing (224 × 224)
- RGB conversion
- Image normalization
- Data augmentation
- Dataset splitting
- Label encoding

### Data Augmentation

- Random Rotation
- Horizontal Flip
- Width Shift
- Height Shift
- Zoom
- Brightness Adjustment

---

## 3️⃣ Exploratory Data Analysis (EDA)

Performed extensive visual analysis including:

- Class distribution
- Sample visualization
- Image dimension analysis
- Image resolution statistics
- Dataset balance inspection

---

## 4️⃣ Deep Learning Models

Developed and evaluated four different architectures.

### Models

- Custom CNN
- MobileNetV2
- ResNet50
- EfficientNetB0

Transfer Learning models were initialized using ImageNet pretrained weights.

---

## 5️⃣ Model Training

Training configuration included:

- TensorFlow / Keras
- Adam Optimizer
- Categorical Crossentropy Loss
- Early Stopping
- Model Checkpoint
- Reduce Learning Rate on Plateau

Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- Classification Report

---

## 6️⃣ Model Comparison

| Model | Test Accuracy |
|---------|--------------|
| Custom CNN | **75.81%** |
| MobileNetV2 | **81.20%** |
| ResNet50 | **81.68%** |
| EfficientNetB0 ⭐ | **81.80%** |

### Final Selected Model

**EfficientNetB0**

Reasons:

- Highest Validation Accuracy
- Highest Test Accuracy
- Better Generalization
- Smaller Model Size
- Fast Inference
- Suitable for Web Deployment

---

## 7️⃣ Flask Web Application

Developed a complete AI-powered web application.

### Features

- Upload oral image
- Real-time disease prediction
- Top-3 predicted classes
- Prediction confidence
- Disease description
- Medical disclaimer
- Responsive UI
- Drag & Drop image upload

---

# 📊 Model Performance

### EfficientNetB0

| Metric | Value |
|---------|--------|
| Train Accuracy | **87.42%** |
| Validation Accuracy | **82.01%** |
| Test Accuracy | **81.80%** |

---

# 📈 Key Findings

- Transfer Learning significantly outperformed the custom CNN.
- EfficientNetB0 achieved the best balance between accuracy and model size.
- ResNet50 delivered comparable performance but required higher computational resources.
- MobileNetV2 offered competitive accuracy with fast inference.
- Hypodontia was consistently the easiest class to classify.
- Calculus and Tooth Discoloration remained the most challenging categories due to visual similarity with other diseases.

---

# 💡 Future Improvements

- Fine-tune additional EfficientNet layers
- Add Grad-CAM visual explanations
- Convert model to TensorFlow Lite
- Deploy using Docker
- Cloud deployment (AWS / Azure)
- User authentication
- Prediction history
- Multi-language support

---

# 🛠️ Technologies Used

## Deep Learning

- Python
- TensorFlow
- Keras
- NumPy
- Pandas

## Data Visualization

- Matplotlib
- Seaborn

## Deployment

- Flask

## Frontend

- HTML5
- CSS3
- JavaScript

## Development

- VS Code
- Git
- GitHub

---

# 📁 Project Structure

```text
OralVision-AI/
│
├── oral-diseases-image-classification.ipynb/
├── models/
│   ├── best_efficientnet.keras
│   ├── ResNet.keras
│   ├── MobileNet.keras
│   └── custom_cnn.keras
│
├── presentation/
│   └── Oral_Disease_Classification.pptx
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── uploads/
│
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── prediction.html
│   └── result.html
│
├── utils/
│   └── predict.py
│
├── app.py
├── App Images/
│
├── requirements.txt
├── README.md
└── sample_oral.png
```

---

# 🚀 Running the Project

## 1. Clone the repository

```bash
git clone https://github.com/mohammedmokhtar77/OralVision-AI.git
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Run Flask

```bash
python app.py
```

---

## 4. Open your browser

```
http://127.0.0.1:5000
```

---

# 🖼️ Application Preview

## 1. Home Page

```
<img src="App Images/home.png" alt="Home Page">
```

---

## 2. Prediction Page

```
<img src="App Images/prediction.png" alt="Prediction Page">
```

---

## 3. Prediction Result

```
<img src="App Images/predictionResult.png" alt="Prediction Result">
<img src="App Images/predictionResult2.png" alt="Prediction Result">
```

---

## 4. About Page
<img src="App Images/about-c.png" alt="About Page">
<img src="App Images/about.png" alt="About Page">

---

# 👨‍💻 Author

**Mohammed Mokhtar**

Computers & AI — Cairo University

AI Engineer & Frontend Developer · Kaggle Master · NLP & Computer Vision · React, Next.js & TypeScript · Scalable & High-Performance AI/Web Apps

