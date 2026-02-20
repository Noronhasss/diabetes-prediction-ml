"""
Database Initialization and Management Module
This module handles SQLite database creation and schema setup for the diabetes prediction application.
"""

import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_db():
    """
    Initialize the SQLite database with required tables.
    Creates users and reports tables if they don't exist.
    Also creates a default admin account.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create reports table (prediction history)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
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
    ''')
    
    # Check if admin exists, if not create default admin
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    
    if not admin:
        # Create default admin account
        admin_password = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@diabetes.com', admin_password, 'admin'))
        print("✓ Default admin account created!")
        print("  Username: admin")
        print("  Password: admin123")
        print("  (Please change this password after first login)")
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully!")

def get_db_connection():
    """
    Create and return a database connection.
    Returns a connection with row factory set to sqlite3.Row for dict-like access.
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_user(username, email, password, role='user'):
    """
    Create a new user in the database.
    
    Args:
        username (str): Unique username
        email (str): Unique email address
        password (str): Plain text password (will be hashed)
        role (str): User role - 'user' or 'admin' (default: 'user')
    
    Returns:
        bool: True if user created successfully, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, role))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user_by_username(username):
    """
    Retrieve user information by username.
    
    Args:
        username (str): Username to search for
    
    Returns:
        dict: User information or None if not found
    """
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def save_prediction(user_id, username, input_data, prediction_result, probability):
    """
    Save a prediction report to the database.
    
    Args:
        user_id (int): User ID
        username (str): Username
        input_data (dict): Dictionary containing all input features
        prediction_result (str): Prediction result (e.g., "Diabetes" or "No Diabetes")
        probability (float): Prediction probability/confidence score
    
    Returns:
        bool: True if saved successfully
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO reports (
                user_id, username, pregnancies, glucose, blood_pressure,
                skin_thickness, insulin, bmi, diabetes_pedigree_function,
                age, prediction_result, probability
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            username,
            input_data['pregnancies'],
            input_data['glucose'],
            input_data['blood_pressure'],
            input_data['skin_thickness'],
            input_data['insulin'],
            input_data['bmi'],
            input_data['diabetes_pedigree_function'],
            input_data['age'],
            prediction_result,
            probability
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving prediction: {e}")
        return False

def get_all_users():
    """
    Get all users from the database.
    
    Returns:
        list: List of all users
    """
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    return users

def get_all_reports():
    """
    Get all prediction reports from the database.
    
    Returns:
        list: List of all reports with user information
    """
    conn = get_db_connection()
    reports = conn.execute('''
        SELECT r.*, u.username, u.email 
        FROM reports r 
        JOIN users u ON r.user_id = u.id 
        ORDER BY r.timestamp DESC
    ''').fetchall()
    conn.close()
    return reports

def get_user_reports(user_id):
    """
    Get all prediction reports for a specific user.
    
    Args:
        user_id (int): User ID
    
    Returns:
        list: List of user's reports
    """
    conn = get_db_connection()
    reports = conn.execute('''
        SELECT * FROM reports 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return reports

def delete_user(user_id):
    """
    Delete a user and all their reports.
    
    Args:
        user_id (int): User ID to delete
    
    Returns:
        bool: True if deleted successfully
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete user's reports first
        cursor.execute('DELETE FROM reports WHERE user_id = ?', (user_id,))
        # Delete user
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False

def delete_report(report_id):
    """
    Delete a specific prediction report.
    
    Args:
        report_id (int): Report ID to delete
    
    Returns:
        bool: True if deleted successfully
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reports WHERE id = ?', (report_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting report: {e}")
        return False

if __name__ == '__main__':
    # Initialize database when run directly
    print("Initializing database...")
    init_db()
