"""
storage.py - Phase 2: Storage
Pulls data from Austin Open Data API and uploads raw CSV to AWS S3.
Organizes files by ingestion date: s3://bucket/raw/YYYY-MM-DD/plan_review_raw.csv
"""

import boto3
import pandas as pd
import requests
from datetime import date

# ── Config ──────────────────────────────────────────────
S3_BUCKET = "yourname-cis4400"   # <-- replace with your S3 bucket name
URL = "https://data.austintexas.gov/resource/6s5u-ims4.json"
# ────────────────────────────────────────────────────────

print("Fetching data...")
df = pd.DataFrame(requests.get(URL, params={"$limit": 200000}).json())
print(f"Records fetched: {len(df)}")

today = date.today().isoformat()
local_file = f"plan_review_raw_{today}.csv"
df.to_csv(local_file, index=False)
print(f"Saved locally: {local_file}")

# Upload to S3
s3 = boto3.client("s3")
s3_key = f"raw/{today}/plan_review_raw.csv"
s3.upload_file(local_file, S3_BUCKET, s3_key)
print(f"Uploaded to s3://{S3_BUCKET}/{s3_key}")
