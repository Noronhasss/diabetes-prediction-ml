import pickle
import numpy as np

# Load model and scaler
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

print("Testing both cases...")
print("="*60)

# Test Case 1 - Should be Likely Diabetes
test1 = np.array([[6, 148, 72, 35, 80, 33.6, 0.627, 50]])
test1_scaled = scaler.transform(test1)
pred1 = model.predict(test1_scaled)[0]
proba1 = model.predict_proba(test1_scaled)[0]

print("\nTest Case 1 (Should be POSITIVE):")
print(f"Input: Pregnancies=6, Glucose=148, BP=72, Skin=35, Insulin=80, BMI=33.6, Pedigree=0.627, Age=50")
print(f"Prediction: {pred1} ({'POSITIVE' if pred1 == 1 else 'NEGATIVE'})")
print(f"Probability [No Diabetes, Has Diabetes]: [{proba1[0]:.4f}, {proba1[1]:.4f}]")
print(f"Confidence: {max(proba1)*100:.2f}%")

# Test Case 2 - Should be Unlikely Diabetes
test2 = np.array([[1, 85, 66, 29, 0, 26.6, 0.351, 31]])
test2_scaled = scaler.transform(test2)
pred2 = model.predict(test2_scaled)[0]
proba2 = model.predict_proba(test2_scaled)[0]

print("\n" + "="*60)
print("\nTest Case 2 (Should be NEGATIVE):")
print(f"Input: Pregnancies=1, Glucose=85, BP=66, Skin=29, Insulin=0, BMI=26.6, Pedigree=0.351, Age=31")
print(f"Prediction: {pred2} ({'POSITIVE' if pred2 == 1 else 'NEGATIVE'})")
print(f"Probability [No Diabetes, Has Diabetes]: [{proba2[0]:.4f}, {proba2[1]:.4f}]")
print(f"Confidence: {max(proba2)*100:.2f}%")

print("\n" + "="*60)

# Load metadata to see which model was used
try:
    with open('model_metadata.pkl', 'rb') as f:
        metadata = pickle.load(f)
    print(f"\nModel Type: {metadata['model_name']}")
    print(f"Training Accuracy: {metadata['accuracy']*100:.2f}%")
except:
    print("\nModel metadata not available")
