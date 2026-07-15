"""
download_from_s3.py - Download Healthcare CSV from AWS S3
==========================================================
What: Downloads the healthcare.csv from S3 back to local storage.
Why:  Simulates fetching raw data from a Data Lake before ETL processing.
How:  Uses boto3 to download the file and returns the local file path.

Pipeline flow:
  S3 Bucket → download_from_s3.py → local CSV → extract.py
"""

import os
import boto3
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()


def download_from_s3(s3_key="raw/healthcare.csv", local_path="data/healthcare_s3.csv"):
    """
    Download a file from AWS S3 to local storage.

    Args:
        s3_key:     S3 object key (source path inside the bucket)
        local_path: Where to save the downloaded file locally

    Returns:
        local_path: Path to the downloaded file
    """
    bucket_name = os.getenv("S3_BUCKET_NAME")
    
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

        s3_client.download_file(bucket_name, s3_key, local_path)
        print(f"[SUCCESS] Downloaded s3://{bucket_name}/{s3_key} → '{local_path}'")
        return local_path

    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        return None


# --- Run directly ---
if __name__ == "__main__":
    download_from_s3()
