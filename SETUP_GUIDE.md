# 🏥 Diabetes Prediction System - Setup & User Guide

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [New Features](#new-features)
3. [Installation & Setup](#installation--setup)
4. [Running the Application](#running-the-application)
5. [User Guide](#user-guide)
6. [Admin Guide](#admin-guide)
7. [Database Structure](#database-structure)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

This is an **enhanced Flask-based Machine Learning application** that predicts diabetes risk based on patient health metrics. The application now includes:
- ✅ User authentication system
- ✅ Role-based access control (User & Admin)
- ✅ Prediction history tracking
- ✅ Admin dashboard for user management
- ✅ Modern medical-themed UI

---

## 🚀 New Features

### Authentication System
- **User Registration**: Create new accounts with email and password
- **Secure Login**: Password hashing using Werkzeug
- **Session Management**: Protected routes with login required
- **Logout**: Secure logout functionality

### User Roles
- **Normal User**: Can make predictions and view their history
- **Admin**: Full access to manage users and view all reports

### User Dashboard
- Enter health metrics for diabetes prediction
- View prediction results with confidence scores
- Access complete prediction history
- Expandable detail views for each prediction

### Admin Dashboard
- View system statistics (users, reports, cases)
- Manage all users (view, delete)
- View all prediction reports
- Delete individual reports

### Database
- SQLite database for persistent storage
- Users table with authentication data
- Reports table with prediction history
- Automatic relationship management

---

## 💾 Installation & Setup

### Step 1: Verify Prerequisites

Make sure you have Python installed and the virtual environment activated.

```powershell
# Check if virtual environment is activated
# You should see (.venv) in your prompt
```

### Step 2: Install Dependencies

All required packages should already be installed. If not, run:

```powershell
pip install Flask Werkzeug scikit-learn numpy pandas joblib
```

### Step 3: Initialize the Database

The database will be automatically created on first run, but you can initialize it manually:

```powershell
python database.py
```

This creates:
- `database.db` file
- Default admin account (username: admin, password: admin123)

### Step 4: Ensure Model Files Exist

Make sure these files are present:
- `model.pkl` (trained ML model)
- `scaler.pkl` (data scaler)
- `model_metadata.pkl` (model information)

If missing, train the model:

```powershell
python model.py
```

---

## 🎮 Running the Application

### Start the Server

```powershell
# Make sure virtual environment is activated
.venv\Scripts\Activate.ps1

# Run the application
python app.py
```

You should see:
```
============================================================
DIABETES PREDICTION WEB APPLICATION
WITH AUTHENTICATION & ADMIN DASHBOARD
============================================================

Default Admin Credentials:
  Username: admin
  Password: admin123

============================================================

Starting Flask server...
Access the application at: http://127.0.0.1:5000
Press CTRL+C to stop the server
============================================================
```

### Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 👤 User Guide

### Creating an Account

1. Click "Register here" on the login page
2. Fill in:
   - Username (minimum 3 characters)
   - Email address
   - Password (minimum 6 characters)
   - Confirm password
3. Click "Create Account"
4. You'll be redirected to login

### Logging In

1. Enter your username and password
2. Click "Login"
3. You'll be redirected to your dashboard

### Making a Prediction

1. After logging in, you'll see the prediction form
2. Enter all required health metrics:
   - **Pregnancies**: Number of times pregnant
   - **Glucose**: Plasma glucose concentration (mg/dL)
   - **Blood Pressure**: Diastolic blood pressure (mm Hg)
   - **Skin Thickness**: Triceps skin fold thickness (mm)
   - **Insulin**: 2-Hour serum insulin (μU/mL)
   - **BMI**: Body mass index (kg/m²)
   - **Diabetes Pedigree Function**: Genetic diabetes function
   - **Age**: Age in years

3. Click "Predict Diabetes"
4. View your prediction result with confidence score
5. The prediction is automatically saved to your history

### Viewing Prediction History

- All your predictions are displayed on the right side of the dashboard
- Click "View Full Details" to see complete input data for each prediction
- Predictions are sorted by most recent first
- Each prediction shows:
  - Date and time
  - Result (Diabetes Detected / No Diabetes)
  - Confidence score
  - Key metrics (Glucose, BMI, Age)

### Logging Out

Click the "Logout" button in the navigation bar to end your session.

---

## 👨‍💼 Admin Guide

### Admin Login

Use the default admin credentials:
- **Username**: admin
- **Password**: admin123

**⚠️ IMPORTANT**: Change this password after first login!

### Admin Dashboard Features

#### Statistics Overview
View real-time statistics:
- Total number of users
- Total prediction reports
- Number of diabetes cases detected
- Number of normal cases

#### User Management
- View all registered users
- See user details (username, email, role, creation date)
- Delete users (except yourself)
- Deleting a user also deletes all their reports

#### Reports Management
- View all prediction reports from all users
- See detailed prediction data
- Click "View" to see full report details in a modal
- Delete individual reports
- Reports show username, metrics, and results

### Managing Users

1. Click the "User Management" tab
2. See the complete list of users
3. To delete a user:
   - Click the "Delete" button next to the user
   - Confirm the deletion
   - User and all their reports will be removed

### Managing Reports

1. Click the "All Reports" tab
2. View all predictions across the system
3. Click "View" to see full details
4. Click the trash icon to delete a report
5. Confirm deletion

---

## 🗄️ Database Structure

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Reports Table
```sql
CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    pregnancies INTEGER,
    glucose INTEGER,
    blood_pressure INTEGER,
    skin_thickness INTEGER,
    insulin INTEGER,
    bmi REAL,
    diabetes_pedigree_function REAL,
    age INTEGER,
    prediction_result TEXT NOT NULL,
    probability REAL NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```

---

## 🔧 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution**: Activate the virtual environment and install dependencies
```powershell
.venv\Scripts\Activate.ps1
pip install Flask Werkzeug scikit-learn numpy pandas joblib
```

### Problem: "ERROR: Model files not found!"

**Solution**: Train the machine learning model first
```powershell
python model.py
```

### Problem: Can't login / "Invalid username or password"

**Solutions**:
1. Double-check your username and password
2. For admin: use username `admin` and password `admin123`
3. If you forgot your password, you'll need to reset the database:
   ```powershell
   Remove-Item database.db
   python database.py
   ```

### Problem: Database errors or corruption

**Solution**: Reinitialize the database
```powershell
# Delete the database file
Remove-Item database.db

# Recreate it
python database.py
```

### Problem: Port 5000 already in use

**Solution**: Either:
1. Stop the other application using port 5000, or
2. Change the port in `app.py`:
   ```python
   app.run(debug=True, host='127.0.0.1', port=5001)  # Change to 5001
   ```

### Problem: Styles not loading / Page looks broken

**Solution**: 
1. Clear browser cache (Ctrl + F5)
2. Verify `static/style.css` exists
3. Check browser console for errors

---

## 📁 Project Structure

```
Predicting Diabetes Progression Using Machine Learning/
│
├── app.py                          # Main Flask application
├── database.py                     # Database management module
├── model.py                        # ML model training script
├── test_model.py                   # Model testing script
│
├── templates/                      # HTML templates
│   ├── base.html                   # Base template (layout)
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── dashboard.html              # User dashboard
│   └── admin_dashboard.html        # Admin dashboard
│
├── static/                         # Static files
│   └── style.css                   # Stylesheet (medical theme)
│
├── model.pkl                       # Trained ML model
├── scaler.pkl                      # Data scaler
├── model_metadata.pkl              # Model information
├── database.db                     # SQLite database
│
├── diabetes.csv                    # Training dataset
├── requirements.txt                # Python dependencies
└── SETUP_GUIDE.md                  # This file
```

---

## 🔐 Security Notes

1. **Change Default Admin Password**: The default admin password is `admin123` - change this immediately!

2. **Secret Key**: In production, change the secret key in `app.py`:
   ```python
   app.secret_key = 'your-unique-secret-key-here'
   ```

3. **Database Backups**: Regularly back up `database.db` to prevent data loss

4. **HTTPS**: In production, use HTTPS instead of HTTP

5. **Password Requirements**: Enforce stronger password policies for production use

---

## 📊 Sample Health Metrics for Testing

Here are some sample values you can use to test predictions:

### High Risk Profile
- Pregnancies: 6
- Glucose: 148
- Blood Pressure: 72
- Skin Thickness: 35
- Insulin: 200
- BMI: 33.6
- Diabetes Pedigree Function: 0.627
- Age: 50

### Low Risk Profile
- Pregnancies: 1
- Glucose: 85
- Blood Pressure: 66
- Skin Thickness: 20
- Insulin: 80
- BMI: 26.6
- Diabetes Pedigree Function: 0.351
- Age: 31

---

## 🎓 Learning Resources

### Understanding the Features

- **BMI**: Body Mass Index = weight (kg) / height (m)²
- **Glucose**: Normal fasting glucose is 70-100 mg/dL
- **Blood Pressure**: Normal diastolic BP is 60-80 mm Hg
- **Diabetes Pedigree Function**: Represents genetic predisposition

### Machine Learning

The system uses a **Random Forest Classifier** with:
- ~79% accuracy
- Probability scores for confidence
- Standardized feature scaling

---

## 👨‍💻 Developer Notes

### Adding New Features

To add new features, follow these patterns:

1. **New Routes**: Add to `app.py` with appropriate decorators
2. **New Templates**: Extend `base.html` for consistency
3. **Database Changes**: Update `database.py` schema and functions
4. **Styling**: Use existing CSS variables for theme consistency

### Customization

- **Colors**: Edit CSS variables in `style.css`
- **Model**: Retrain with different algorithms in `model.py`
- **Validation**: Add custom validators in route handlers

---

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Check browser console for frontend errors
4. Verify all files are present and correct

---

## ✅ Quick Start Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Model files present (run `python model.py` if needed)
- [ ] Database initialized
- [ ] Application running on http://127.0.0.1:5000
- [ ] Can access login page
- [ ] Can login with admin credentials
- [ ] Can create new user account
- [ ] Can make predictions
- [ ] Can view prediction history
- [ ] Admin can access admin dashboard

---

## 🎉 You're All Set!

Your enhanced diabetes prediction system is ready to use. Enjoy the new features and improved interface!

**Remember**: This is a demonstration project. For real medical use:
- Consult healthcare professionals
- Use verified medical data
- Implement additional security measures
- Follow healthcare data regulations (HIPAA, etc.)

---

*Last Updated: February 19, 2026*
