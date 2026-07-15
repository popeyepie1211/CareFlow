"""
load.py - Load Transformed Data into MySQL
=============================================
What: Connects to MySQL and inserts cleaned patient records.
Why:  This is the LOAD step of the ETL pipeline.
How:  Uses mysql-connector-python with parameterized INSERT statements.

Pipeline flow:
  extract.py -> transform.py -> load.py -> MySQL (patients table)

Prerequisites:
  1. MySQL server running on localhost
  2. .env file with database credentials
  3. database/schema.sql defines the patients table
"""

import os
import mysql.connector
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()


def get_db_connection():
    """
    Create and return a MySQL database connection.
    Reads credentials from environment variables.
    """
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
    )
    print("[INFO] Connected to MySQL")
    return connection


def setup_database(cursor):
    """
    Create the database and patients table if they don't exist.
    Reads and executes the schema.sql file.
    """
    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS healthcare_db")
    cursor.execute("USE healthcare_db")

    # Create patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id                 INT AUTO_INCREMENT PRIMARY KEY,
            age                INT NOT NULL,
            gender             VARCHAR(10),
            medical_condition  VARCHAR(100),
            admission_type     VARCHAR(20),
            insurance_provider VARCHAR(50),
            billing_amount     DECIMAL(10, 2),
            test_result        VARCHAR(20),
            length_of_stay     INT
        )
    """)
    cursor.execute("TRUNCATE TABLE patients")
    print("[INFO] Schema verified and table truncated")


def insert_records(cursor, df):
    """
    Insert all rows from the DataFrame into the patients table.
    Uses parameterized queries to prevent SQL injection.
    """
    insert_query = """
        INSERT INTO patients
            (age, gender, medical_condition, admission_type,
             insurance_provider, billing_amount, test_result, length_of_stay)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Convert DataFrame rows to list of tuples
    records = [
        (
            int(row["age"]),
            row["gender"],
            row["medical_condition"],
            row["admission_type"],
            row["insurance_provider"],
            round(float(row["billing_amount"]), 2),
            row["test_result"],
            int(row["length_of_stay"]),
        )
        for _, row in df.iterrows()
    ]

    print(f"[INFO] Inserting {len(records)} rows...")
    cursor.executemany(insert_query, records)
    print("[SUCCESS] Insert completed")


def load_data(df):
    """
    Main load function: connect to MySQL, setup schema, insert data.

    Args:
        df: Transformed DataFrame with columns matching the patients table
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        setup_database(cursor)
        insert_records(cursor, df)

        connection.commit()
        cursor.close()
        connection.close()
        print("[INFO] Connection closed")

    except mysql.connector.Error as e:
        print(f"[ERROR] MySQL error: {e}")


# --- Run directly to test ---
if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(__file__))

    from extract import extract_data
    from transform import transform_data

    raw_df = extract_data()
    if raw_df is not None:
        clean_df = transform_data(raw_df)
        load_data(clean_df)
