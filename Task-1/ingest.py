import os
import json
import psycopg2
from psycopg2.extras import execute_values

# Constants from environment or defaults
DB_NAME = os.getenv("POSTGRES_DB", "wearipedia")
DB_USER = os.getenv("POSTGRES_USER", "wearipedia_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "19768003")
DB_HOST = os.getenv("TSDB_HOST", "timescaledb")
DB_PORT = os.getenv("TSDB_PORT", "5432")
DATA_DIR = os.getenv("EXTRACTED_DIR", "./extracted_data")

RAW_TABLE = "raw_data"

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
    )

def create_table():
    query = f"""
    CREATE TABLE IF NOT EXISTS {RAW_TABLE} (
        user_id TEXT NOT NULL,
        metric TEXT NOT NULL,
        timestamp TIMESTAMPTZ NOT NULL,
        value DOUBLE PRECISION,
        PRIMARY KEY (user_id, metric, timestamp)
    );
    """
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()

def insert_records(records):
    if not records:
        return

    query = f"""
    INSERT INTO {RAW_TABLE} (user_id, metric, timestamp, value)
    VALUES %s
    ON CONFLICT (user_id, metric, timestamp) DO NOTHING;
    """
    values = [
        (rec["user_id"], rec["metric"], rec["timestamp"], rec["value"])
        for rec in records
        if all(k in rec for k in ["user_id", "metric", "timestamp", "value"])
    ]

    with connect_db() as conn:
        with conn.cursor() as cur:
            execute_values(cur, query, values)
            conn.commit()

def ingest_all():
    print("-- Ingestion Started --")
    create_table()

    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(DATA_DIR, filename)
        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                print(f"Processing {filename}...")
                insert_records(data)
            else:
                print(f"Skipping {filename} (unsupported structure)")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("-- Ingestion Complete --")

if __name__ == "__main__":
    ingest_all()