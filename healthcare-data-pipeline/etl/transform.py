"""
transform.py - Clean and Transform Healthcare Data
=====================================================
What: Performs data cleaning and feature engineering on raw patient data.
Why:  This is the TRANSFORM step of the ETL pipeline.
How:  Removes duplicates, handles missing values, standardizes text,
      converts dates, drops unnecessary columns, and engineers one feature.

Pipeline flow:
  extract.py → transform.py → load.py → MySQL

Transformations performed:
  1. Remove duplicate rows
  2. Handle missing values (drop rows with nulls in key columns)
  3. Convert date columns to datetime format
  4. Standardize text columns (strip whitespace, title case)
  5. Drop unnecessary columns (Name, Doctor, Hospital, etc.)
  6. Engineer feature: length_of_stay (discharge - admission in days)
"""

import pandas as pd


def remove_duplicates(df):
    """Remove duplicate rows from the DataFrame."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"   Duplicates removed: {before - after}")
    return df


def handle_missing_values(df):
    """Drop rows with missing values in critical columns."""
    critical_columns = ["Age", "Gender", "Medical Condition", "Billing Amount"]
    before = len(df)
    df = df.dropna(subset=critical_columns)
    after = len(df)
    print(f"   Rows dropped (missing values): {before - after}")
    return df


def convert_dates(df):
    """Convert date columns to datetime format."""
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
    df["Discharge Date"] = pd.to_datetime(df["Discharge Date"])
    print("   Date columns converted to datetime")
    return df


def standardize_text(df):
    """Strip whitespace and apply title case to text columns."""
    text_columns = ["Gender", "Medical Condition", "Admission Type",
                    "Insurance Provider", "Test Results"]

    for col in text_columns:
        df[col] = df[col].astype(str).str.strip().str.title()

    print(f"   Standardized {len(text_columns)} text columns")
    return df


def drop_unnecessary_columns(df):
    """Drop columns not needed for analysis or ML."""
    columns_to_drop = ["Name", "Doctor", "Hospital", "Blood Type",
                       "Room Number", "Medication"]
    df = df.drop(columns=columns_to_drop, errors="ignore")
    print(f"   Dropped {len(columns_to_drop)} unnecessary columns")
    return df


def engineer_features(df):
    """Create length_of_stay feature (days between admission and discharge)."""
    df["length_of_stay"] = (df["Discharge Date"] - df["Date of Admission"]).dt.days
    print(f"   Engineered feature: length_of_stay (mean={df['length_of_stay'].mean():.1f} days)")
    return df


def rename_columns(df):
    """Rename columns to match the MySQL schema (snake_case)."""
    column_mapping = {
        "Age": "age",
        "Gender": "gender",
        "Medical Condition": "medical_condition",
        "Admission Type": "admission_type",
        "Insurance Provider": "insurance_provider",
        "Billing Amount": "billing_amount",
        "Test Results": "test_result",
    }
    df = df.rename(columns=column_mapping)
    return df


def transform_data(df):
    """
    Run all transformation steps on the raw DataFrame.

    Args:
        df: Raw DataFrame from extract step

    Returns:
        Cleaned and transformed DataFrame ready for loading
    """
    print("[INFO] Starting data transformation...")

    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = convert_dates(df)
    df = standardize_text(df)
    df = drop_unnecessary_columns(df)
    df = engineer_features(df)
    df = rename_columns(df)

    # Keep only the columns that match our MySQL schema
    final_columns = ["age", "gender", "medical_condition", "admission_type",
                     "insurance_provider", "billing_amount", "test_result",
                     "length_of_stay"]
    df = df[final_columns]

    print(f"[SUCCESS] Transformation complete: {len(df)} rows, {len(df.columns)} columns")
    return df


# --- Run directly to test ---
if __name__ == "__main__":
    from extract import extract_data

    raw_df = extract_data()
    if raw_df is not None:
        clean_df = transform_data(raw_df)
        print("\nSample output:")
        print(clean_df.head(3))
        print("\nColumn types:")
        print(clean_df.dtypes)
