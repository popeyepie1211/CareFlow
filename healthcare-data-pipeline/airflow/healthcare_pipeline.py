"""
healthcare_pipeline.py - Apache Airflow DAG
==============================================
What: Defines the healthcare data pipeline as an Airflow DAG.
Why:  Demonstrates workflow orchestration using Apache Airflow.
How:  Uses PythonOperator to call each pipeline step sequentially.

This DAG mirrors the same steps as run_pipeline.py:
    Extract → Transform → Load → Analytics → Train Model

Note:
    This DAG exists to demonstrate Airflow knowledge.
    The project can also be run locally via: python run_pipeline.py
"""

import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Add project root to path so Airflow can find our modules
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


# --- Task Functions ---

def task_extract():
    """Extract raw data from CSV."""
    from etl.extract import extract_data
    extract_data(os.path.join(PROJECT_ROOT, "data/healthcare.csv"))


def task_transform():
    """Transform and clean the extracted data."""
    from etl.extract import extract_data
    from etl.transform import transform_data
    raw_df = extract_data(os.path.join(PROJECT_ROOT, "data/healthcare.csv"))
    transform_data(raw_df)


def task_load():
    """Load transformed data into MySQL."""
    from etl.extract import extract_data
    from etl.transform import transform_data
    from etl.load import load_data
    raw_df = extract_data(os.path.join(PROJECT_ROOT, "data/healthcare.csv"))
    clean_df = transform_data(raw_df)
    load_data(clean_df)


def task_analytics():
    """Run SQL analytics queries on the loaded data."""
    from run_pipeline import run_sql_analytics
    run_sql_analytics()


def task_train_model():
    """Train and save the Random Forest model."""
    from ml.train import load_data_from_mysql, prepare_features, train_model, save_model
    df = load_data_from_mysql()
    if df is not None:
        X, y, encoder = prepare_features(df)
        model, acc, roc = train_model(X, y)
        save_model(model, os.path.join(PROJECT_ROOT, "ml/model.joblib"))


# --- DAG Definition ---

default_args = {
    "owner": "data-engineer",
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}

with DAG(
    dag_id="healthcare_data_pipeline",
    default_args=default_args,
    description="Healthcare ETL, Analytics, and ML Pipeline",
    schedule_interval=None,
    catchup=False,
) as dag:

    extract     = PythonOperator(task_id="extract",       python_callable=task_extract)
    transform   = PythonOperator(task_id="transform",     python_callable=task_transform)
    load        = PythonOperator(task_id="load_mysql",    python_callable=task_load)
    analytics   = PythonOperator(task_id="sql_analytics", python_callable=task_analytics)
    train       = PythonOperator(task_id="train_model",   python_callable=task_train_model)

    # Linear pipeline: Extract → Transform → Load → Analytics → Train
    extract >> transform >> load >> analytics >> train
