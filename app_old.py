"""
Flask Web Application for Diabetes Prediction
This application loads the trained ML model and provides a web interface
for users to input patient data and get diabetes predictions.
"""

# Import necessary libraries
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

# Initialize Flask application
app = Flask(__name__)

# Load the trained model and scaler
print("Loading model and scaler...")
try:
    # Load the saved model
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    print("✓ Model loaded successfully!")
    
    # Load the saved scaler
    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    print("✓ Scaler loaded successfully!")
    
    # Load model metadata (optional)
    try:
        with open('model_metadata.pkl', 'rb') as meta_file:
            metadata = pickle.load(meta_file)
        print(f"✓ Model: {metadata['model_name']} (Accuracy: {metadata['accuracy']*100:.2f}%)")
    except:
        print("⚠ Model metadata not found")
        
except FileNotFoundError:
    print("\n" + "="*60)
    print("ERROR: Model files not found!")
    print("="*60)
    print("Please run 'python model.py' first to train and save the model.")
    print("="*60)
    exit()

# Define the home route
@app.route('/')
def home():
    """
    Render the home page with the input form
    """
    return render_template('index.html')

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle form submission and return prediction result
    """
    try:
        # Get form data
        # Extract all 8 features from the form
        pregnancies = float(request.form['pregnancies'])
        glucose = float(request.form['glucose'])
        blood_pressure = float(request.form['blood_pressure'])
        skin_thickness = float(request.form['skin_thickness'])
        insulin = float(request.form['insulin'])
        bmi = float(request.form['bmi'])
        diabetes_pedigree = float(request.form['diabetes_pedigree'])
        age = float(request.form['age'])
        
        # Create feature array in the correct order
        # Order: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age
        features = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, 
                            insulin, bmi, diabetes_pedigree, age]])
        
        # Scale the input features using the saved scaler
        features_scaled = scaler.transform(features)
        
        # Get prediction probability first
        prediction_proba = model.predict_proba(features_scaled)[0]
        
        # Use a lower threshold (0.45) for better sensitivity
        # This helps catch borderline cases that might have diabetes
        prediction = 1 if prediction_proba[1] >= 0.45 else 0
        
        # Determine the result
        if prediction == 1:
            result = "Diabetes Positive"
            probability = prediction_proba[1] * 100  # Probability of having diabetes
            risk_level = "High Risk"
            result_class = "positive"
        else:
            result = "Diabetes Negative"
            probability = prediction_proba[0] * 100  # Probability of not having diabetes
            risk_level = "Low Risk"
            result_class = "negative"
        
        # Return the result to the template
        return render_template('index.html', 
                             prediction_text=result,
                             probability=f"{probability:.2f}%",
                             risk_level=risk_level,
                             result_class=result_class,
                             show_result=True)
    
    except Exception as e:
        # Handle errors gracefully
        error_message = f"Error: {str(e)}"
        return render_template('index.html', 
                             prediction_text="Error in prediction",
                             error_message=error_message,
                             show_result=True,
                             result_class="error")

# API endpoint for predictions (optional - for future use)
@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    API endpoint for predictions
    Accepts JSON data and returns JSON response
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        # Extract features
        features = np.array([[
            data['pregnancies'],
            data['glucose'],
            data['blood_pressure'],
            data['skin_thickness'],
            data['insulin'],
            data['bmi'],
            data['diabetes_pedigree'],
            data['age']
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        prediction_proba = model.predict_proba(features_scaled)[0]
        
        # Prepare response
        response = {
            'prediction': int(prediction),
            'result': 'Diabetes Positive' if prediction == 1 else 'Diabetes Negative',
            'probability': float(prediction_proba[1] * 100),
            'confidence': float(max(prediction_proba) * 100)
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Run the Flask application
if __name__ == '__main__':
    print("\n" + "="*60)
    print("DIABETES PREDICTION WEB APPLICATION")
    print("="*60)
    print("\nStarting Flask server...")
    print("Access the application at: http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    # Run the app in debug mode
    app.run(debug=True, host='127.0.0.1', port=5000)
