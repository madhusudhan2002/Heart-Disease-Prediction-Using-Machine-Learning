import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
import joblib
import json

def train_models():
    df = pd.read_csv('heart_disease_data.csv')

    # Features
    X = df[['Age', 'Cholesterol', 'Blood_Pressure', 'Max_Heart_Rate', 'BMI', 'Blood_Sugar']]
    y = df['Target']

    # ✅ Stratified split (IMPORTANT FIX)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ✅ SMOTE (balanced dataset)
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

    print("After SMOTE:", pd.Series(y_resampled).value_counts())

    # ✅ FINAL TUNED RANDOM FOREST (IMPORTANT)
    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=7,
        min_samples_split=20,
        min_samples_leaf=8,
        max_features='sqrt',
        class_weight='balanced',
        random_state=42
    )

    # Train model
    model.fit(X_resampled, y_resampled)

    # Predictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    sens = recall_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)

    print(f"Accuracy: {acc*100:.2f}%")
    print(f"Sensitivity: {sens*100:.2f}%")
    print(f"AUC: {auc*100:.2f}%")

    # Save model
    joblib.dump(model, 'random_model.joblib')

    metrics = {
        'accuracy': acc,
        'sensitivity': sens,
        'auc': auc
    }

    with open('metrics.json', 'w') as f:
        json.dump(metrics, f)

    print("✅ Final tuned Random Forest model saved successfully.")

if __name__ == "__main__":
    train_models()