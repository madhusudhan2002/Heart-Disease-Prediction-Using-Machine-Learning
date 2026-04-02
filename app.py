import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import joblib
import pandas as pd
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = 'super_secret_heart_key'

# ---------------- MAIL CONFIG ----------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'madhusudhanreddy51998@gmail.com'
app.config['MAIL_PASSWORD'] = 'REAL_16_CHARACTER_PASSWORD'

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)

DATABASE = 'database.db'

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with app.app_context():
        db = get_db()

        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL
            )
        ''')

init_db()

# ---------------- LOAD RANDOM FOREST MODEL ----------------
rf_model = None
metrics = {}

try:
    print("Loading Random Forest model...")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "random_model.joblib")
    metrics_path = os.path.join(BASE_DIR, "metrics.json")

    rf_model = joblib.load(model_path)

    print("Random Forest model loaded successfully!")

    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics = json.load(f)

except Exception as e:
    print("MODEL LOADING ERROR:", e)

# ---------------- HOME ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']

        hashed_pw = generate_password_hash(password)

        db = get_db()

        try:
            db.execute(
                'INSERT INTO users (name,email,password,user_type) VALUES (?,?,?,?)',
                (name, email, hashed_pw, user_type)
            )
            db.commit()

            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))

        except sqlite3.IntegrityError:
            flash('Email already registered.', 'danger')
            return redirect(url_for('signup'))

    return render_template('signup.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        db = get_db()

        user = db.execute(
            'SELECT * FROM users WHERE email=?',
            (email,)
        ).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['user_type'] = user['user_type']
            return redirect(url_for('predict_page'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

# ---------------- FORGOT PASSWORD ----------------
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':

        email = request.form['email']
        db = get_db()

        user = db.execute(
            'SELECT * FROM users WHERE email=?',
            (email,)
        ).fetchone()

        if user:
            token = serializer.dumps(email, salt='password-reset-salt')

            reset_link = url_for(
                'reset_password',
                token=token,
                _external=True
            )

            print("\n====== PASSWORD RESET LINK ======")
            print(reset_link)
            print("=================================\n")

            flash('Reset link generated. Check terminal.', 'success')
        else:
            flash('Email not registered.', 'danger')

        return redirect(url_for('login'))

    return render_template('forgot_password.html')

# ---------------- RESET PASSWORD ----------------
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(
            token,
            salt='password-reset-salt',
            max_age=3600
        )
    except:
        flash('Reset link expired or invalid.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form['password']
        hashed_pw = generate_password_hash(new_password)

        db = get_db()

        db.execute(
            'UPDATE users SET password=? WHERE email=?',
            (hashed_pw, email)
        )
        db.commit()

        flash('Password updated successfully.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

# ---------------- PREDICTION PAGE ----------------
@app.route('/predict_page')
def predict_page():
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))

    return render_template('predict.html', name=session.get('name'))

# ---------------- PREDICTION API ----------------
@app.route('/predict', methods=['POST'])
def predict():

    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    if rf_model is None:
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded. Check random_forest_model.joblib'
        })

    try:
        data = request.get_json()

        required_fields = [
            'Age',
            'Cholesterol',
            'Blood_Pressure',
            'Max_Heart_Rate',
            'BMI',
            'Blood_Sugar'
        ]

        for field in required_fields:
            if field not in data or data[field] == '':
                return jsonify({'status': 'error', 'message': f'Missing {field}'})

        features = [
            float(data['Age']),
            float(data['Cholesterol']),
            float(data['Blood_Pressure']),
            float(data['Max_Heart_Rate']),
            float(data['BMI']),
            float(data['Blood_Sugar'])
        ]

        input_df = pd.DataFrame([features], columns=[
            'Age',
            'Cholesterol',
            'Blood_Pressure',
            'Max_Heart_Rate',
            'BMI',
            'Blood_Sugar'
        ])

        # Prediction
        pred = int(rf_model.predict(input_df)[0])
        prob = float(rf_model.predict_proba(input_df)[0][1])

        confidence = prob if pred == 1 else (1 - prob)

        # ---------------- RESULTS ----------------
        if pred == 1:
            result = "Heart Disease Detected"
            risk_level = "High Risk"
            advice = "Immediate medical consultation recommended."
            final_decision = "Needs Attention"
        else:
            result = "No Heart Disease Detected"
            risk_level = "Healthy"
            advice = "Maintain healthy lifestyle."
            final_decision = "Good Condition"

        return jsonify({
            'status': 'success',
            'result': result,
            'confidence_score': f"{confidence*100:.2f}%",
            'risk_level': risk_level,
            'advice': advice,
            'final_decision': final_decision
        })

    except Exception as e:
        print(" PREDICTION ERROR:", e)
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)