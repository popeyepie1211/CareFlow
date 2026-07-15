"""
app.py - Healthcare Data Pipeline Dashboard
==============================================
What: Streamlit dashboard showing pipeline results and analytics.
Why:  Provides a visual summary of the data engineering pipeline output.
How:  Queries MySQL for live data and reads model metrics from JSON.

Usage:
    streamlit run dashboard/app.py
"""

import os
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_db_connection():
    """Connect to MySQL and return connection."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="healthcare_db",
    )


def run_query(query):
    """Run a SQL query and return results as a DataFrame."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows, columns=columns)


def load_metrics():
    """Load model metrics from JSON file."""
    metrics_path = os.path.join(os.path.dirname(__file__), "..", "ml", "metrics.json")
    try:
        with open(metrics_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"accuracy": 0.0, "roc_auc": 0.0}


# --- Page Config ---
st.set_page_config(page_title="Healthcare Pipeline Dashboard", layout="wide")
st.title("Healthcare Data Pipeline Dashboard")
st.markdown("Results from the end-to-end data engineering pipeline.")

# --- KPI Cards ---
total_patients = run_query("SELECT COUNT(*) AS total FROM patients")
avg_billing = run_query("SELECT ROUND(AVG(billing_amount), 2) AS avg_bill FROM patients")
most_common = run_query(
    "SELECT medical_condition, COUNT(*) AS cnt FROM patients "
    "GROUP BY medical_condition ORDER BY cnt DESC LIMIT 1"
)
metrics = load_metrics()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Patients", f"{total_patients['total'][0]:,}")
col2.metric("Avg Billing", f"${float(avg_billing['avg_bill'][0]):,.2f}")
col3.metric("Most Common Disease", most_common["medical_condition"][0])
col4.metric("Model Accuracy", f"{metrics['accuracy']:.2%}")
col5.metric("ROC AUC", f"{metrics['roc_auc']:.4f}")

st.markdown("---")

# --- Charts ---
chart_col1, chart_col2 = st.columns(2)

# Admissions by Type Chart
with chart_col1:
    st.subheader("Admissions by Type")
    admissions = run_query(
        "SELECT admission_type, COUNT(*) AS total "
        "FROM patients GROUP BY admission_type ORDER BY total DESC"
    )
    fig1, ax1 = plt.subplots()
    ax1.bar(admissions["admission_type"], admissions["total"], color=["#4e79a7", "#f28e2b", "#e15759"])
    ax1.set_xlabel("Admission Type")
    ax1.set_ylabel("Count")
    st.pyplot(fig1)

# Disease Distribution Chart
with chart_col2:
    st.subheader("Disease Distribution")
    diseases = run_query(
        "SELECT medical_condition, COUNT(*) AS total "
        "FROM patients GROUP BY medical_condition ORDER BY total DESC"
    )
    fig2, ax2 = plt.subplots()
    ax2.barh(diseases["medical_condition"], diseases["total"], color="#76b7b2")
    ax2.set_xlabel("Count")
    st.pyplot(fig2)

# --- Footer ---
st.markdown("---")
st.caption("Healthcare Data Engineering Pipeline | Built with Python, MySQL, and Streamlit")
