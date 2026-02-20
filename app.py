"""
Enhanced Flask Web Application for Diabetes Prediction
Includes user authentication, role-based access control, and prediction history management.
"""

# Import necessary libraries
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import pickle
import numpy as np
import os
from functools import wraps
from datetime import datetime

# Import database functions
from database import (
    init_db, get_db_connection, create_user, get_user_by_username,
    save_prediction, get_all_users, get_all_reports, get_user_reports,
    delete_user, delete_report
)

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # IMPORTANT: Change this in production!

# Initialize database
init_db()

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

# ==================== DECORATORS ====================

def login_required(f):
    """
    Decorator to protect routes that require authentication.
    Redirects to login page if user is not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to protect admin-only routes.
    Redirects to dashboard if user is not an admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """
    Home page - redirects to dashboard if logged in, otherwise shows login
    """
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration page.
    Handles both GET (display form) and POST (process registration).
    """
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'danger')
            return render_template('register.html')
        
        # Create user
        if create_user(username, email, password):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists!', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page.
    Handles both GET (display form) and POST (process login).
    """
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validation
        if not username or not password:
            flash('Username and password are required!', 'danger')
            return render_template('login.html')
        
        # Check credentials
        user = get_user_by_username(username)
        
        if user and check_password_hash(user['password_hash'], password):
            # Set session variables
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['role'] = user['role']
            
            flash(f'Welcome back, {user["username"]}!', 'success')
            
            # Redirect based on role
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Logout the current user by clearing the session.
    """
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('login'))

# ==================== USER DASHBOARD ROUTES ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """
    User dashboard page.
    Shows prediction form and user's prediction history.
    """
    # Get user's prediction history
    user_reports = get_user_reports(session['user_id'])
    
    # Convert Row objects to dictionaries
    reports_list = [dict(report) for report in user_reports]
    
    return render_template('dashboard.html', 
                          username=session['username'],
                          reports=reports_list)

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    """
    Handle diabetes prediction request.
    Processes input data, makes prediction, and saves to database.
    """
    try:
        # Get input data from form
        input_data = {
            'pregnancies': int(request.form.get('pregnancies')),
            'glucose': int(request.form.get('glucose')),
            'blood_pressure': int(request.form.get('blood_pressure')),
            'skin_thickness': int(request.form.get('skin_thickness')),
            'insulin': int(request.form.get('insulin')),
            'bmi': float(request.form.get('bmi')),
            'diabetes_pedigree_function': float(request.form.get('diabetes_pedigree_function')),
            'age': int(request.form.get('age'))
        }
        
        # Prepare data for prediction
        features = np.array([[
            input_data['pregnancies'],
            input_data['glucose'],
            input_data['blood_pressure'],
            input_data['skin_thickness'],
            input_data['insulin'],
            input_data['bmi'],
            input_data['diabetes_pedigree_function'],
            input_data['age']
        ]])
        
        # Scale the features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        prediction_proba = model.predict_proba(features_scaled)[0]
        
        # Interpret results
        result = "Diabetes Detected" if prediction == 1 else "No Diabetes"
        probability = float(max(prediction_proba) * 100)
        
        # Save prediction to database
        save_prediction(
            user_id=session['user_id'],
            username=session['username'],
            input_data=input_data,
            prediction_result=result,
            probability=probability
        )
        
        flash(f'Prediction completed: {result} (Confidence: {probability:.2f}%)', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        flash(f'Error making prediction: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

# ==================== ADMIN DASHBOARD ROUTES ====================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """
    Admin dashboard page.
    Shows all users and all prediction reports.
    """
    users = get_all_users()
    reports = get_all_reports()
    
    # Convert Row objects to dictionaries for JSON serialization
    users_list = [dict(user) for user in users]
    reports_list = [dict(report) for report in reports]
    
    # Calculate statistics
    total_users = len(users_list)
    total_reports = len(reports_list)
    diabetes_cases = sum(1 for r in reports_list if 'Diabetes Detected' in r['prediction_result'])
    
    stats = {
        'total_users': total_users,
        'total_reports': total_reports,
        'diabetes_cases': diabetes_cases,
        'normal_cases': total_reports - diabetes_cases
    }
    
    return render_template('admin_dashboard.html',
                          username=session['username'],
                          users=users_list,
                          reports=reports_list,
                          stats=stats)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    """
    Admin route to delete a user.
    Prevents deletion of own account.
    """
    if user_id == session['user_id']:
        flash('You cannot delete your own account!', 'danger')
    elif delete_user(user_id):
        flash('User deleted successfully!', 'success')
    else:
        flash('Error deleting user!', 'danger')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_report/<int:report_id>', methods=['POST'])
@admin_required
def admin_delete_report(report_id):
    """
    Admin route to delete a prediction report.
    """
    if delete_report(report_id):
        flash('Report deleted successfully!', 'success')
    else:
        flash('Error deleting report!', 'danger')
    
    return redirect(url_for('admin_dashboard'))

# ==================== API ROUTES (Optional - for AJAX) ====================

@app.route('/api/predict', methods=['POST'])
@login_required
def api_predict():
    """
    API endpoint for making predictions via AJAX.
    Returns JSON response.
    """
    try:
        data = request.get_json()
        
        # Prepare data for prediction
        features = np.array([[
            data['pregnancies'],
            data['glucose'],
            data['blood_pressure'],
            data['skin_thickness'],
            data['insulin'],
            data['bmi'],
            data['diabetes_pedigree_function'],
            data['age']
        ]])
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        prediction_proba = model.predict_proba(features_scaled)[0]
        
        result = "Diabetes Detected" if prediction == 1 else "No Diabetes"
        probability = float(max(prediction_proba) * 100)
        
        # Save to database
        save_prediction(
            user_id=session['user_id'],
            username=session['username'],
            input_data=data,
            prediction_result=result,
            probability=probability
        )
        
        return jsonify({
            'success': True,
            'result': result,
            'probability': probability
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("DIABETES PREDICTION WEB APPLICATION")
    print("WITH AUTHENTICATION & ADMIN DASHBOARD")
    print("="*60)
    print("\nDefault Admin Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\n" + "="*60)
    print("\nStarting Flask server...")
    print("Access the application at: http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    # Run the app
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)