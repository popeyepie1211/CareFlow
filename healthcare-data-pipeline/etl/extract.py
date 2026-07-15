"""
extract.py - Extract Data from CSV
====================================
What: Reads the healthcare CSV file into a Pandas DataFrame.
Why:  This is the EXTRACT step of the ETL pipeline.
How:  Uses pandas.read_csv() to load data and prints basic info.

Pipeline flow:
  S3 Download → extract.py → transform.py → load.py → MySQL
"""

import pandas as pd


def extract_data(file_path="data/healthcare.csv"):
    """
    Read healthcare CSV and return a DataFrame.

    Args:
        file_path: Path to the CSV file (default: local data folder)

    Returns:
        DataFrame with raw patient data
    """
    try:
        df = pd.read_csv(file_path)
        print(f"[SUCCESS] Extracted {len(df)} rows and {len(df.columns)} columns")
        print(f"   Columns: {list(df.columns)}")
        return df

    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        return None


# --- Run directly to test ---
if __name__ == "__main__":
    df = extract_data()
    if df is not None:
        print("\nFirst 3 rows:")
        print(df.head(3))
