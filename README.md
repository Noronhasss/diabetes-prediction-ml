# 🩺 Predicting Diabetes Progression Using Machine Learning

A complete Machine Learning web application that predicts diabetes progression using the Pima Indians Diabetes Dataset. This project implements Logistic Regression and Random Forest models with a clean Flask web interface.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation Guide](#installation-guide)
- [Usage Instructions](#usage-instructions)
- [Dataset Information](#dataset-information)
- [Model Performance](#model-performance)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Project Overview

This project demonstrates the application of Machine Learning in healthcare by predicting the likelihood of diabetes based on diagnostic measurements. The system:

1. **Trains and evaluates** two ML models (Logistic Regression & Random Forest)
2. **Compares model performance** using multiple metrics
3. **Saves the best model** for production use
4. **Provides a web interface** for real-time predictions

---

## ✨ Features

### Machine Learning Features
- ✅ Data preprocessing with missing value handling
- ✅ Feature scaling using StandardScaler
- ✅ Train-test split (70-30)
- ✅ Model comparison (Logistic Regression vs Random Forest)
- ✅ Comprehensive evaluation metrics:
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - ROC-AUC
- ✅ Automatic best model selection
- ✅ Model persistence using pickle

### Web Application Features
- 🌐 Clean and modern user interface
- 📱 Responsive design (mobile-friendly)
- 📊 Real-time diabetes prediction
- 📈 Probability score display
- ⚠️ Risk level assessment
- 🎨 Professional gradient design
- ✅ Form validation
- 🔄 Easy-to-use interface

---

## 🛠️ Technologies Used

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **scikit-learn** - Machine learning
- **pandas** - Data manipulation
- **NumPy** - Numerical computing

### Frontend
- **HTML5**
- **CSS3** (with modern gradients and animations)
- **JavaScript** (for form validation)

---

## 📁 Project Structure

```
Predicting Diabetes Progression Using Machine Learning/
│
├── app.py                      # Flask web application
├── model.py                    # ML model training script
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── templates/
│   └── index.html             # Web interface template
│
├── static/
│   └── style.css              # CSS styling
│
├── diabetes.csv               # Dataset (to be added by user)
├── model.pkl                  # Trained model (generated after training)
├── scaler.pkl                 # Fitted scaler (generated after training)
└── model_metadata.pkl         # Model information (generated after training)
```

---

## 📥 Installation Guide

### Step 1: Prerequisites
Make sure you have Python 3.8 or higher installed on your system.

Check your Python version:
```bash
python --version
```

### Step 2: Clone or Download the Project
Download this project folder to your computer.

### Step 3: Download the Dataset
Download the **Pima Indians Diabetes Dataset** and save it as `diabetes.csv` in the project folder.

**Dataset Source:** 
- [Kaggle - Pima Indians Diabetes Database](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database)

The dataset should have these columns:
- Pregnancies
- Glucose
- BloodPressure
- SkinThickness
- Insulin
- BMI
- DiabetesPedigreeFunction
- Age
- Outcome (0 or 1)

### Step 4: Install Dependencies
Open a terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

This will install all required Python packages:
- Flask
- scikit-learn
- pandas
- numpy
- joblib

---

## 🚀 Usage Instructions

### Step 1: Train the Machine Learning Model

First, train the models by running:

```bash
python model.py
```

**What this does:**
- Loads and preprocesses the diabetes dataset
- Handles missing values
- Splits data into training and testing sets
- Trains Logistic Regression and Random Forest models
- Evaluates both models with multiple metrics
- Compares performance and selects the best model
- Saves the best model, scaler, and metadata as pickle files

**Expected Output:**
```
Loading diabetes dataset...
Dataset loaded successfully!
...
Training models...
Model comparison results...
Best Model: Random Forest
Accuracy: 78.26%
✓ Model saved as 'model.pkl'
✓ Scaler saved as 'scaler.pkl'
```

### Step 2: Run the Flask Web Application

After training, start the web server:

```bash
python app.py
```

**Expected Output:**
```
✓ Model loaded successfully!
✓ Scaler loaded successfully!
...
* Running on http://127.0.0.1:5000
```

### Step 3: Access the Web Interface

Open your web browser and go to:
```
http://127.0.0.1:5000
```

### Step 4: Make Predictions

1. Fill in the patient information form with all 8 features:
   - **Pregnancies**: Number of times pregnant
   - **Glucose**: Plasma glucose concentration (mg/dL)
   - **Blood Pressure**: Diastolic blood pressure (mm Hg)
   - **Skin Thickness**: Triceps skin fold thickness (mm)
   - **Insulin**: 2-Hour serum insulin (μU/mL)
   - **BMI**: Body mass index (kg/m²)
   - **Diabetes Pedigree Function**: Family history score (0.0-2.5)
   - **Age**: Age in years

2. Click **"🔍 Predict Diabetes"**

3. View the prediction result:
   - **Diabetes Positive** or **Diabetes Negative**
   - Confidence level (probability percentage)
   - Risk assessment

---

## 📊 Dataset Information

### Pima Indians Diabetes Dataset

**Source:** National Institute of Diabetes and Digestive and Kidney Diseases

**Objective:** Predict whether a patient has diabetes based on diagnostic measurements.

**Features (8):**
1. **Pregnancies**: Number of pregnancies
2. **Glucose**: Plasma glucose concentration
3. **BloodPressure**: Diastolic blood pressure
4. **SkinThickness**: Triceps skin fold thickness
5. **Insulin**: 2-Hour serum insulin
6. **BMI**: Body mass index
7. **DiabetesPedigreeFunction**: Diabetes pedigree function
8. **Age**: Age in years

**Target Variable:**
- **Outcome**: 0 (No Diabetes) or 1 (Diabetes)

**Total Samples:** 768
- Diabetes Cases: ~268 (35%)
- Non-Diabetes Cases: ~500 (65%)

---

## 📈 Model Performance

### Logistic Regression
- **Accuracy**: ~77%
- **Precision**: ~0.72
- **Recall**: ~0.60
- **F1 Score**: ~0.65
- **ROC-AUC**: ~0.82

### Random Forest Classifier
- **Accuracy**: ~78%
- **Precision**: ~0.75
- **Recall**: ~0.62
- **F1 Score**: ~0.68
- **ROC-AUC**: ~0.83

*Note: Actual performance may vary based on data preprocessing and random state.*

---

## 🎨 Screenshots

### Home Page
The main interface with input form for patient data.

### Prediction Result - Negative
Clean display showing "Diabetes Negative" with confidence score.

### Prediction Result - Positive
Alert display showing "Diabetes Positive" with risk assessment.

---

## 🔧 Troubleshooting

### Issue: "diabetes.csv not found"
**Solution:** Download the dataset from Kaggle and place it in the project folder.

### Issue: "ModuleNotFoundError"
**Solution:** Install dependencies using `pip install -r requirements.txt`

### Issue: "Model not found"
**Solution:** Run `python model.py` first to train and save the model.

### Issue: Port 5000 already in use
**Solution:** Change the port in app.py:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

---

## 💡 Future Enhancements

- [ ] Add more ML models (SVM, XGBoost, Neural Networks)
- [ ] Implement cross-validation
- [ ] Add feature importance visualization
- [ ] Create data visualization dashboard
- [ ] Add user authentication
- [ ] Store predictions in a database
- [ ] Deploy to cloud (Heroku, AWS, Azure)
- [ ] Add API endpoints for mobile apps

---

## 👥 Contributing

This is a college project for educational purposes. Feel free to fork and enhance!

---

## 📝 License

This project is open-source and available for educational purposes.

---

## ⚠️ Disclaimer

**Important:** This is a machine learning prediction tool created for educational and demonstration purposes only. It should **NOT** be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical decisions.

---

## 👨‍💻 Author

**College Project - Machine Learning**
- **Course**: Machine Learning / Data Science
- **Year**: 2026
- **Purpose**: Educational Project Submission

---

## 📞 Contact & Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments
3. Verify all installation steps were followed

---

## 🙏 Acknowledgments

- **Dataset**: National Institute of Diabetes and Digestive and Kidney Diseases
- **Libraries**: scikit-learn, Flask, pandas, NumPy
- **Inspiration**: Healthcare applications of Machine Learning

---

**Happy Learning! 🎓**

---

### Quick Start Summary

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train the model
python model.py

# 3. Run the web app
python app.py

# 4. Open browser
# Navigate to: http://127.0.0.1:5000
```

---

*Last Updated: February 2026*
