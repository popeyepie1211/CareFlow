"""
upload_to_s3.py - Upload Healthcare CSV to AWS S3
==================================================
What: Uploads the local healthcare.csv file to an AWS S3 bucket.
Why:  Simulates raw data ingestion into cloud storage (S3 as Data Lake).
How:  Uses boto3 to connect to S3 and upload the file.

This is the FIRST step in the pipeline:
  healthcare.csv → S3 Bucket → (download) → ETL → MySQL
"""

import os
import boto3
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()


def upload_to_s3(file_path, bucket_name=None, s3_key="raw/healthcare.csv"):
    """
    Upload a local CSV file to AWS S3.

    Args:
        file_path:   Path to the local CSV file
        bucket_name: S3 bucket name (reads from .env if not provided)
        s3_key:      S3 object key (destination path inside the bucket)
    """
    bucket_name = bucket_name or os.getenv("S3_BUCKET_NAME")
    
    if not bucket_name:
        print("[ERROR] S3_BUCKET_NAME is not set in .env")
        return None

    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "ap-south-1"),
        )

        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"[SUCCESS] Uploaded '{file_path}' to s3://{bucket_name}/{s3_key}")

    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")


# --- Run directly ---
if __name__ == "__main__":
    upload_to_s3("data/healthcare.csv")
