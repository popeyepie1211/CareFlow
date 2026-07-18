<div align="center">

# 🏥 CareFlow — Healthcare Data Engineering Pipeline

**An end-to-end data pipeline that ingests, transforms, stores, analyzes, and visualizes 10,000+ patient records — from raw CSV to interactive dashboard.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![AWS S3](https://img.shields.io/badge/AWS_S3-Data_Lake-FF9900?style=flat&logo=amazons3&logoColor=white)](https://aws.amazon.com/s3/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Airflow](https://img.shields.io/badge/Apache_Airflow-Orchestration-017CEE?style=flat&logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)
[![Scikit‑learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=flat&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)

</div>

---

## 📌 What Is This?

**CareFlow** is a production-style data engineering project that simulates a real-world healthcare analytics workflow. It demonstrates the full lifecycle of data — from ingestion in a cloud data lake, through ETL processing and warehousing, to machine learning predictions and business intelligence dashboards.

> **Built to showcase**: Data Engineering, ETL Design, Cloud Integration, SQL Analytics, ML Pipelines, and Data Visualization — the core skills expected in Data Engineer and ML Engineer roles.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CareFlow Pipeline                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   📂 Raw CSV (10K records)                                  │
│        │                                                    │
│        ▼                                                    │
│   ☁️  AWS S3 ──────────── Data Lake (Raw Zone)              │
│        │                                                    │
│        ▼                                                    │
│   🔄 ETL Pipeline (Python + Pandas)                         │
│        ├── Extract   → Read from S3 / local CSV             │
│        ├── Transform → Clean, standardize, feature eng.     │
│        └── Load      → Parameterized insert into MySQL      │
│        │                                                    │
│        ▼                                                    │
│   🗄️  MySQL Database ─── Structured Storage                 │
│        │                                                    │
│        ├──────────────────────────┐                         │
│        ▼                          ▼                         │
│   📊 SQL Analytics           🤖 ML Model                    │
│   (5 BI queries)             (Random Forest)                │
│        │                          │                         │
│        └──────────┬───────────────┘                         │
│                   ▼                                         │
│            📈 Streamlit Dashboard                           │
│            (Live KPIs + Charts)                             │
│                                                             │
│   ⏰ Orchestration: Apache Airflow DAG                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|:------|:-----------|:--------|
| **Language** | Python 3.10+ | Core pipeline logic |
| **Data Processing** | Pandas, NumPy | Transformation & feature engineering |
| **Cloud Storage** | AWS S3 (boto3) | Data lake — raw data ingestion |
| **Database** | MySQL | Structured data warehouse |
| **Orchestration** | Apache Airflow | DAG-based pipeline scheduling |
| **Machine Learning** | Scikit-learn | Random Forest classification |
| **Dashboard** | Streamlit | Interactive analytics UI |
| **Visualization** | Matplotlib | Charts & model evaluation plots |
| **Config** | python-dotenv | Environment-based credential mgmt |

---

## ✨ Key Features

### 🔄 ETL Pipeline
- **Extract** — Reads 10,000 patient records from CSV (locally or via S3 download)
- **Transform** — Deduplication, null handling, text standardization, date parsing, and feature engineering (`length_of_stay`)
- **Load** — Parameterized SQL inserts into MySQL with auto-schema creation

### ☁️ AWS S3 Integration
- Upload/download scripts for cloud-based data lake pattern
- Environment-variable-driven configuration (no hardcoded credentials)

### 📊 SQL Analytics
Five business intelligence queries answering questions like:
- What is the average billing amount across all patients?
- Which medical conditions are most prevalent?
- How do billing patterns differ by disease?

### 🤖 Machine Learning
- **Model**: Random Forest Classifier (100 estimators)
- **Target**: Patient test results (Normal / Abnormal / Inconclusive)
- **Features**: Age, gender, condition, admission type, insurance, billing, length of stay
- **Evaluation**: Accuracy, ROC AUC (weighted, OVR), confusion matrix, classification report
- **Persistence**: Model serialized via Joblib for downstream prediction

### 📈 Interactive Dashboard
Streamlit app displaying live KPIs (total patients, avg billing, model accuracy) and charts (admissions by type, disease distribution) — all powered by real-time MySQL queries.

### ⏰ Airflow Orchestration
Production-ready DAG definition with five sequential tasks mirroring the full pipeline, demonstrating workflow scheduling and dependency management.

---

## 📁 Project Structure

```
healthcare-data-pipeline/
│
├── aws/
│   ├── upload_to_s3.py            # Push raw data to S3
│   └── download_from_s3.py        # Pull data from S3
│
├── etl/
│   ├── extract.py                 # Read CSV → DataFrame
│   ├── transform.py               # Clean + feature engineering
│   └── load.py                    # DataFrame → MySQL
│
├── database/
│   └── schema.sql                 # MySQL table definition
│
├── sql/
│   └── analytics.sql              # 5 analytical queries
│
├── ml/
│   ├── train.py                   # Train & evaluate model
│   ├── predict.py                 # Inference with saved model
│   ├── model.joblib               # Serialized model (generated)
│   └── metrics.json               # Accuracy & ROC AUC (generated)
│
├── airflow/
│   └── healthcare_pipeline.py     # Airflow DAG definition
│
├── dashboard/
│   └── app.py                     # Streamlit dashboard
│
├── data/
│   └── healthcare.csv             # Source dataset (10K records)
│
├── run_pipeline.py                # One-command pipeline runner
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- MySQL Server
- AWS account *(optional — pipeline works locally without S3)*

### 1. Clone & Install

```bash
git clone https://github.com/popeyepie1211/CareFlow.git
cd CareFlow/healthcare-data-pipeline
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password

# AWS (optional)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your-bucket-name
```

### 3. Run the Pipeline

```bash
python run_pipeline.py
```

This executes the complete pipeline in sequence:

```
Extract → Transform → Load → SQL Analytics → Train Model
```

### 4. Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

### 5. (Optional) Airflow Orchestration

```bash
pip install apache-airflow
# Copy airflow/healthcare_pipeline.py to your Airflow dags/ folder
# Start scheduler + webserver, then trigger the DAG
```

---

## 📊 Pipeline Output

| Metric | Value |
|:-------|:------|
| Records Processed | 10,000+ |
| Transformations | 6 (dedup, nulls, dates, text, columns, features) |
| SQL Analytics Queries | 5 |
| ML Model | Random Forest (100 trees) |
| Evaluation | Accuracy + ROC AUC + Confusion Matrix |
| Dashboard KPIs | 5 live metrics |

---

## 🗺️ Roadmap

- [ ] Data validation layer with Great Expectations
- [ ] Incremental loading (CDC pattern) instead of full reload
- [ ] Structured logging with Python's `logging` module
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Data versioning with DVC
- [ ] Scale transforms with Apache Spark
- [ ] Deploy to AWS with S3 triggers + Lambda

---

## 📄 License

This project is for educational and portfolio purposes.

---

<div align="center">

**Built with ❤️ by [Ashwin](https://github.com/popeyepie1211)**

*If you found this useful, consider giving it a ⭐*

</div>
