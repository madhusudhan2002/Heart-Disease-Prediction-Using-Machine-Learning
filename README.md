❤️ Heart Disease Prediction System
📌 Overview

The Heart Disease Prediction System is a machine learning-powered web application that predicts the likelihood of heart disease using patient medical data. It combines predictive modeling with a user-friendly interface to support early diagnosis and healthcare decision-making.

🚀 Features
User authentication system (Login / Signup / Password Reset)
Interactive dashboard for user navigation
Heart disease prediction using trained ML models
Ensemble and Random Forest models (.joblib)
Data preprocessing and feature handling
Real-time prediction via web interface
Persistent storage using SQLite database
Clean UI using HTML templates
🛠️ Tech Stack
👨‍💻 Programming
Python
📚 Libraries
Pandas
NumPy
Scikit-learn
Joblib
🌐 Backend
Flask
🗄️ Database
SQLite (database.db)
🎨 Frontend
HTML (Jinja Templates)
📊 Dataset
File: heart_disease_data.csv
Contains clinical attributes such as:
Age, Sex
Chest Pain Type
Blood Pressure
Cholesterol
ECG Results
Heart Rate
Exercise-induced Angina
⚙️ Project Workflow
Data Collection (heart_disease_data.csv)
Data Preprocessing & Cleaning
Model Training (train_model.py)
Model Saving (.joblib)
Model Evaluation (metrics.json)
Flask App Integration (app.py)
User Interaction via Web Interface
📈 Model Performance
Metric	Value
Accuracy	92.21%
Sensitivity (Recall)	90.48%
AUC Score	0.987

👉 The model shows high accuracy and excellent AUC, indicating strong predictive performance and good class separation.

🖥️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/heart-disease-prediction.git
cd heart-disease-prediction
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Run the application
python app.py
4️⃣ Open in browser
http://127.0.0.1:5000/
📂 Project Structure
heart-disease-prediction/
│
├── app.py                  # Flask application
├── train_model.py         # Model training script
├── metrics.json           # Model evaluation results
├── heart_disease_data.csv # Dataset
├── database.db            # SQLite database
├── ensemble_model.joblib  # Ensemble trained model
├── random_model.joblib    # Random Forest model
├── requirements.txt       # Dependencies
│
├── templates/             # Frontend HTML pages
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── predict.html
│   ├── forgot_password.html
│   └── reset_password.html
│
└── README.md
🎯 Use Cases
Early detection of heart disease risk
Clinical decision support systems
Healthcare data analytics
🔮 Future Enhancements
Add real-time patient monitoring integration
Deploy on cloud (AWS / Render / Heroku)
Add API endpoints for external integration
Improve model using deep learning
⚠️ Notes
The venv/ folder should be excluded using .gitignore
Models are pre-trained and loaded directly for prediction
🤝 Contributing

Contributions are welcome! Fork the repo and submit a pull request.

📜 License

This project is licensed under the MIT License.

👨‍💻 Author

Undela Madhusudhan Reddy