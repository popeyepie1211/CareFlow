"""
train.py - Train Random Forest Model
=======================================
What: Trains a Random Forest classifier to predict patient test results.
Why:  Demonstrates ML skills as part of the data pipeline.
How:  Reads data from MySQL, encodes features, trains model, evaluates,
      and saves the trained model using Joblib.

Target Variable: test_result (Normal, Abnormal, Inconclusive)

Pipeline flow:
  MySQL -> train.py -> model.joblib -> predict.py
"""

import os
import pandas as pd
import mysql.connector
import joblib
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

# Load credentials from .env
load_dotenv()


def load_data_from_mysql():
    """Fetch patient data from MySQL for model training."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD"),
            database="healthcare_db",
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        conn.close()
        print(f"[INFO] Loaded {len(df)} rows from MySQL")
        return df

    except mysql.connector.Error as e:
        print(f"[ERROR] MySQL error: {e}")
        return None


def prepare_features(df):
    """
    Encode categorical columns and split into features (X) and target (y).
    Target: test_result (Normal / Abnormal / Inconclusive)
    """
    # Encode categorical columns
    label_encoders = {}
    categorical_cols = ["gender", "medical_condition", "admission_type",
                        "insurance_provider"]

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # Encode target variable
    target_encoder = LabelEncoder()
    df["test_result"] = target_encoder.fit_transform(df["test_result"])

    # Split features and target
    feature_cols = ["age", "gender", "medical_condition", "admission_type",
                    "insurance_provider", "billing_amount", "length_of_stay"]
    X = df[feature_cols]
    y = df["test_result"]

    print(f"[INFO] Features: {feature_cols}")
    print(f"[INFO] Target classes: {list(target_encoder.classes_)}")
    return X, y, target_encoder


def train_model(X, y):
    """Train a Random Forest classifier and evaluate performance."""
    # Train/Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"[INFO] Training set: {len(X_train)} rows")
    print(f"[INFO] Test set: {len(X_test)} rows")

    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("[SUCCESS] Model trained")

    # Predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)

    # Evaluation Metrics
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba, multi_class="ovr", average="weighted")
    conf_matrix = confusion_matrix(y_test, y_pred)

    print(f"\n--- Model Evaluation ---")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"ROC AUC:   {roc_auc:.4f}")
    print(f"\nConfusion Matrix:\n{conf_matrix}")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

    return model, accuracy, roc_auc


def save_model(model, filepath="ml/model.joblib"):
    """Save the trained model to disk using Joblib."""
    try:
        joblib.dump(model, filepath)
        print(f"[SUCCESS] Model saved to '{filepath}'")
    except Exception as e:
        print(f"[ERROR] Failed to save model: {e}")


# --- Run directly to train ---
if __name__ == "__main__":
    df = load_data_from_mysql()
    if df is not None:
        X, y, target_encoder = prepare_features(df)
        model, accuracy, roc_auc = train_model(X, y)
        save_model(model)
