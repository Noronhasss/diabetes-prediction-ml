"""
Machine Learning Model Training Script
This script trains and evaluates Logistic Regression and Random Forest models
for diabetes prediction using the Pima Indians Diabetes Dataset.
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# Load the dataset
print("Loading diabetes dataset...")
try:
    df = pd.read_csv('diabetes.csv')
    print(f"Dataset loaded successfully! Shape: {df.shape}")
    print("\nFirst few rows of the dataset:")
    print(df.head())
except FileNotFoundError:
    print("ERROR: diabetes.csv not found!")
    print("Please download the Pima Indians Diabetes Dataset and save it as 'diabetes.csv'")
    print("Dataset available at: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database")
    exit()

# Display basic information about the dataset
print("\n" + "="*60)
print("Dataset Information:")
print("="*60)
print(df.info())
print("\nDataset Statistics:")
print(df.describe())

# Check for missing values
print("\n" + "="*60)
print("Missing Values Check:")
print("="*60)
print(df.isnull().sum())

# Handle missing values (zeros in some columns represent missing values)
# Columns where 0 is not a valid value
columns_with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

print("\n" + "="*60)
print("Handling Missing Values (zeros):")
print("="*60)

# Replace 0 with NaN for specific columns
for col in columns_with_zeros:
    zero_count = (df[col] == 0).sum()
    print(f"{col}: {zero_count} zero values found")
    df[col] = df[col].replace(0, np.nan)

# Fill NaN with median values
for col in columns_with_zeros:
    df[col] = df[col].fillna(df[col].median())
    print(f"{col}: Filled with median value {df[col].median():.2f}")

# Separate features and target variable
X = df.drop('Outcome', axis=1)  # Features
y = df['Outcome']  # Target variable (0 = No Diabetes, 1 = Diabetes)

print("\n" + "="*60)
print("Features and Target:")
print("="*60)
print(f"Features (X): {X.columns.tolist()}")
print(f"Target (y): Outcome (0 = No Diabetes, 1 = Diabetes)")
print(f"Total samples: {len(X)}")
print(f"Diabetes cases: {y.sum()} ({y.sum()/len(y)*100:.2f}%)")
print(f"Non-diabetes cases: {len(y)-y.sum()} ({(len(y)-y.sum())/len(y)*100:.2f}%)")

# Split the data into training and testing sets (70% training, 30% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

print("\n" + "="*60)
print("Train-Test Split (70-30):")
print("="*60)
print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# Feature Scaling using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n" + "="*60)
print("Feature Scaling Applied (StandardScaler)")
print("="*60)

# ============================================
# Model 1: Logistic Regression
# ============================================
print("\n" + "="*60)
print("TRAINING MODEL 1: LOGISTIC REGRESSION")
print("="*60)

# Initialize and train Logistic Regression model
lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train_scaled, y_train)
print("✓ Logistic Regression model trained successfully!")

# Make predictions
y_pred_lr = lr_model.predict(X_test_scaled)
y_pred_proba_lr = lr_model.predict_proba(X_test_scaled)[:, 1]

# Evaluate Logistic Regression
lr_accuracy = accuracy_score(y_test, y_pred_lr)
lr_precision = precision_score(y_test, y_pred_lr)
lr_recall = recall_score(y_test, y_pred_lr)
lr_f1 = f1_score(y_test, y_pred_lr)
lr_roc_auc = roc_auc_score(y_test, y_pred_proba_lr)

print("\nLogistic Regression Results:")
print(f"  • Accuracy:  {lr_accuracy:.4f} ({lr_accuracy*100:.2f}%)")
print(f"  • Precision: {lr_precision:.4f}")
print(f"  • Recall:    {lr_recall:.4f}")
print(f"  • F1 Score:  {lr_f1:.4f}")
print(f"  • ROC-AUC:   {lr_roc_auc:.4f}")

# ============================================
# Model 2: Random Forest Classifier
# ============================================
print("\n" + "="*60)
print("TRAINING MODEL 2: RANDOM FOREST CLASSIFIER")
print("="*60)

# Initialize and train Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
rf_model.fit(X_train_scaled, y_train)
print("✓ Random Forest model trained successfully!")

# Make predictions
y_pred_rf = rf_model.predict(X_test_scaled)
y_pred_proba_rf = rf_model.predict_proba(X_test_scaled)[:, 1]

# Evaluate Random Forest
rf_accuracy = accuracy_score(y_test, y_pred_rf)
rf_precision = precision_score(y_test, y_pred_rf)
rf_recall = recall_score(y_test, y_pred_rf)
rf_f1 = f1_score(y_test, y_pred_rf)
rf_roc_auc = roc_auc_score(y_test, y_pred_proba_rf)

print("\nRandom Forest Results:")
print(f"  • Accuracy:  {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")
print(f"  • Precision: {rf_precision:.4f}")
print(f"  • Recall:    {rf_recall:.4f}")
print(f"  • F1 Score:  {rf_f1:.4f}")
print(f"  • ROC-AUC:   {rf_roc_auc:.4f}")

# ============================================
# Model Comparison
# ============================================
print("\n" + "="*60)
print("MODEL COMPARISON")
print("="*60)

# Create comparison table
comparison_df = pd.DataFrame({
    'Metric': ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC-AUC'],
    'Logistic Regression': [lr_accuracy, lr_precision, lr_recall, lr_f1, lr_roc_auc],
    'Random Forest': [rf_accuracy, rf_precision, rf_recall, rf_f1, rf_roc_auc]
})

print(comparison_df.to_string(index=False))

# Determine the best model based on accuracy
print("\n" + "="*60)
print("SELECTING BEST MODEL")
print("="*60)

if rf_accuracy > lr_accuracy:
    best_model = rf_model
    best_model_name = "Random Forest"
    best_accuracy = rf_accuracy
else:
    best_model = lr_model
    best_model_name = "Logistic Regression"
    best_accuracy = lr_accuracy

print(f"Best Model: {best_model_name}")
print(f"Best Accuracy: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")

# ============================================
# Save the best model and scaler
# ============================================
print("\n" + "="*60)
print("SAVING MODEL AND SCALER")
print("="*60)

# Save the best model
with open('model.pkl', 'wb') as model_file:
    pickle.dump(best_model, model_file)
print("✓ Best model saved as 'model.pkl'")

# Save the scaler
with open('scaler.pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)
print("✓ Scaler saved as 'scaler.pkl'")

# Save model metadata
metadata = {
    'model_name': best_model_name,
    'accuracy': best_accuracy,
    'features': X.columns.tolist()
}
with open('model_metadata.pkl', 'wb') as meta_file:
    pickle.dump(metadata, meta_file)
print("✓ Model metadata saved as 'model_metadata.pkl'")

print("\n" + "="*60)
print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("="*60)
print("\nYou can now run the Flask application:")
print("  python app.py")
print("\nAnd access it at: http://127.0.0.1:5000")
