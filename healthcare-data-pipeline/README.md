# Healthcare Data Engineering Pipeline

A complete end-to-end **Data Engineering** project demonstrating the lifecycle of a healthcare data pipeline — from raw data ingestion through ETL processing, database storage, SQL analytics, machine learning, and visualization.

## Architecture

```
Healthcare Dataset (CSV)
        │
        ▼
   AWS S3 (Raw Data Storage)
        │
        ▼
   Python ETL (Pandas)
   ├── Extract
   ├── Transform (Clean + Feature Engineering)
   └── Load
        │
        ▼
   MySQL Database (patients table)
        │
        ├──────────────────┐
        ▼                  ▼
   SQL Analytics      Random Forest Model
        │                  │
        └──────┬───────────┘
               ▼
       Streamlit Dashboard
```

**Orchestration:** Apache Airflow DAG (optional)

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Data Processing | Pandas, NumPy |
| Database | MySQL |
| Cloud Storage | AWS S3 (boto3) |
| Orchestration | Apache Airflow |
| Machine Learning | Scikit-learn (Random Forest) |
| Dashboard | Streamlit |
| Visualization | Matplotlib |

## Folder Structure

```
healthcare-data-pipeline/
│
├── data/
│   └── healthcare.csv          # Raw healthcare dataset (10,000 records)
│
├── aws/
│   ├── upload_to_s3.py         # Upload CSV to AWS S3
│   └── download_from_s3.py     # Download CSV from S3
│
├── etl/
│   ├── extract.py              # Read CSV into DataFrame
│   ├── transform.py            # Clean, standardize, engineer features
│   └── load.py                 # Insert records into MySQL
│
├── database/
│   └── schema.sql              # MySQL table definition
│
├── sql/
│   └── analytics.sql           # Analytical SQL queries
│
├── ml/
│   ├── train.py                # Train Random Forest classifier
│   ├── predict.py              # Load model and make predictions
│   ├── model.joblib            # Saved trained model (generated)
│   └── metrics.json            # Model metrics (generated)
│
├── airflow/
│   └── healthcare_pipeline.py  # Airflow DAG definition
│
├── dashboard/
│   └── app.py                  # Streamlit dashboard
│
├── run_pipeline.py             # Local pipeline runner (recommended)
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/healthcare-data-pipeline.git
cd healthcare-data-pipeline
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials.

## AWS S3 Configuration

1. Create an AWS account and an S3 bucket.
2. Generate an Access Key from IAM.
3. Update `.env` with your credentials:

```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your-bucket-name
```

4. Upload data to S3:

```bash
python aws/upload_to_s3.py
```

5. Download data from S3:

```bash
python aws/download_from_s3.py
```

## MySQL Configuration

1. Install MySQL and start the server.
2. Update `.env` with your MySQL credentials:

```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=healthcare_db
```

3. (Optional) Create the database manually:

```bash
mysql -u root -p < database/schema.sql
```

The pipeline will also create the database and table automatically.

## Running the Pipeline

### Option 1: Local Runner (Recommended)

```bash
python run_pipeline.py
```

This executes the complete pipeline:
- Extract → Transform → Load → SQL Analytics → Train Model

### Option 2: Apache Airflow

The project includes an Airflow DAG at `airflow/healthcare_pipeline.py` that orchestrates the same pipeline.

To use it:

1. Install Airflow: `pip install apache-airflow`
2. Copy the DAG to your Airflow dags folder
3. Start the Airflow webserver and scheduler
4. Trigger the `healthcare_data_pipeline` DAG

> **Note:** The local runner (`run_pipeline.py`) is provided for easy demonstration. The Airflow DAG demonstrates orchestration concepts and is suitable for production-style scheduling.

## Running the Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard displays:
- Total Patients, Average Billing, Most Common Disease
- Model Accuracy and ROC AUC Score
- Admissions by Type chart
- Disease Distribution chart

## Pipeline Details

### ETL Process

| Step | File | Description |
|---|---|---|
| Extract | `etl/extract.py` | Reads 10,000 patient records from CSV |
| Transform | `etl/transform.py` | Removes duplicates, handles missing values, standardizes text, engineers `length_of_stay` feature |
| Load | `etl/load.py` | Inserts cleaned data into MySQL using parameterized queries |

### SQL Analytics

Five analytical queries in `sql/analytics.sql`:
1. Average Billing Amount
2. Most Common Disease
3. Admissions by Type
4. Insurance Provider Distribution
5. Average Billing by Disease

### Machine Learning

- **Algorithm:** Random Forest Classifier
- **Target:** Test Result (Normal / Abnormal / Inconclusive)
- **Features:** Age, Gender, Medical Condition, Admission Type, Insurance Provider, Billing Amount, Length of Stay
- **Evaluation:** Accuracy, ROC AUC, Confusion Matrix, Classification Report
- **Model Persistence:** Saved using Joblib

## Resume Highlights

- Built an **end-to-end data engineering pipeline** processing 10,000+ healthcare records
- Implemented **ETL pipeline** using Python and Pandas with data cleaning, standardization, and feature engineering
- Designed **AWS S3** integration for raw data ingestion (Data Lake pattern)
- Created **MySQL** database schema and loaded data using parameterized SQL queries
- Wrote **SQL analytics** queries for business intelligence insights
- Trained a **Random Forest** classifier and persisted the model using Joblib
- Orchestrated pipeline tasks using **Apache Airflow** DAG with PythonOperator
- Built an interactive **Streamlit dashboard** for pipeline result visualization
- Followed **Data Engineering best practices**: environment-based configuration, modular code, separation of concerns

## Interview Questions

1. **Walk me through your data pipeline architecture.**
2. **How did you handle data cleaning in the ETL process?**
3. **Why did you choose MySQL over other databases?**
4. **How does your Airflow DAG orchestrate the pipeline?**
5. **What feature engineering did you perform?**
6. **How do you handle credentials and configuration?**
7. **What would you change for a production deployment?**
8. **How would you scale this pipeline for larger datasets?**
9. **Explain your SQL analytics queries and what insights they provide.**
10. **How did you evaluate your machine learning model?**

## Future Improvements

- Add **data validation** using Great Expectations
- Implement **incremental loading** instead of full table reload
- Add **logging** with Python's logging module
- Deploy to **AWS** with S3 triggers and Lambda functions
- Add **unit tests** for ETL functions
- Implement **CI/CD** pipeline with GitHub Actions
- Add **data versioning** with DVC
- Scale with **Apache Spark** for larger datasets

## License

This project is for educational and portfolio purposes.
