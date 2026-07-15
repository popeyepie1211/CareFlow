"""
run_pipeline.py - Healthcare Data Pipeline Runner
=====================================================
What: Executes the complete data engineering pipeline locally.
Why:  Provides a simple way to run the entire pipeline without Airflow.
How:  Imports and calls each pipeline step sequentially.

Usage:
    python run_pipeline.py

Pipeline Steps:
    1. Extract   → Read CSV into DataFrame
    2. Transform  → Clean, standardize, engineer features
    3. Load       → Insert into MySQL
    4. Analytics  → Run SQL queries on the loaded data
    5. Train      → Train Random Forest model and save it
"""

import os
import sys
import json
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data
from ml.train import load_data_from_mysql, prepare_features, train_model, save_model
from aws.upload_to_s3 import upload_to_s3
from aws.download_from_s3 import download_from_s3


def run_sql_analytics():
    """Run analytical queries on the patients table and print results."""
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="healthcare_db",
    )
    cursor = conn.cursor()

    queries = {
        "Average Billing": "SELECT ROUND(AVG(billing_amount), 2) FROM patients",
        "Most Common Disease": "SELECT medical_condition, COUNT(*) AS cnt FROM patients GROUP BY medical_condition ORDER BY cnt DESC LIMIT 1",
        "Admissions by Type": "SELECT admission_type, COUNT(*) FROM patients GROUP BY admission_type ORDER BY COUNT(*) DESC",
    }

    print("\n--- SQL Analytics Results ---")
    for name, query in queries.items():
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"  {name}: {rows}")

    cursor.close()
    conn.close()
    print("[SUCCESS] SQL analytics completed")


def save_metrics(accuracy, roc_auc):
    """Save model metrics to JSON for the dashboard to read."""
    metrics = {"accuracy": round(accuracy, 4), "roc_auc": round(roc_auc, 4)}
    with open("ml/metrics.json", "w") as f:
        json.dump(metrics, f)
    print(f"[INFO] Metrics saved to ml/metrics.json")


def main():
    """Execute the complete healthcare data pipeline."""
    print("=" * 60)
    print("  Healthcare Data Engineering Pipeline")
    print("=" * 60)

    data_file = "data/healthcare.csv"

    # Step 0: AWS S3 (Optional)
    if os.getenv("S3_BUCKET_NAME"):
        print("\n>> Step 0: AWS S3 Sync")
        upload_to_s3(data_file)
        downloaded = download_from_s3()
        if downloaded:
            data_file = downloaded

    # Step 1: Extract
    print("\n>> Step 1: Extract")
    raw_df = extract_data(data_file)
    if raw_df is None:
        return

    # Step 2: Transform
    print("\n>> Step 2: Transform")
    clean_df = transform_data(raw_df)

    # Step 3: Load into MySQL
    print("\n>> Step 3: Load into MySQL")
    load_data(clean_df)

    # Step 4: SQL Analytics
    print("\n>> Step 4: SQL Analytics")
    run_sql_analytics()

    # Step 5: Train Model
    print("\n>> Step 5: Train Random Forest Model")
    df = load_data_from_mysql()
    if df is not None:
        X, y, target_encoder = prepare_features(df)
        model, accuracy, roc_auc = train_model(X, y)
        save_model(model)
        save_metrics(accuracy, roc_auc)

    print("\n" + "=" * 60)
    print("  Pipeline completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
