import os
import json
import psycopg2
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB", "wearipedia"),
    "user": os.getenv("POSTGRES_USER", "wearipedia_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "19768003"),
    "host": os.getenv("TSDB_HOST", "timescaledb"),
    "port": os.getenv("TSDB_PORT", "5432"),
}

AGG_WINDOWS = {
    "data_1m": "1min",
    "data_1h": "1h",
    "data_1d": "1d"
}

EXTRACTED_DIR = "extracted_data"

def insert_raw_and_aggregates(records):
    print(f"Inserting {len(records)} raw records and computing aggregates...")
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    for row in records:
        cur.execute(
            """
            INSERT INTO raw_data (user_id, metric, timestamp, value)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
            """,
            (row["user_id"], row["metric"], row["timestamp"], row["value"])
        )

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    for table, rule in AGG_WINDOWS.items():
        print(f"Aggregating into {table} using {rule} interval...")
        df_agg = (
            df.groupby(["user_id", "metric", pd.Grouper(key="timestamp", freq=rule)])
            .agg(avg_value=("value", "mean"))
            .reset_index()
        )

        for _, row in df_agg.iterrows():
            cur.execute(
                f"""
                INSERT INTO {table} (user_id, metric, timestamp, avg_value)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (row.user_id, row.metric, row.timestamp, row.avg_value)
            )

    conn.commit()
    cur.close()
    conn.close()
    print("All data inserted and aggregated.")


if __name__ == "__main__":
    print("Starting ingestion_update pipeline...")
    files = [f for f in os.listdir(EXTRACTED_DIR) if f.endswith(".json")]

    for file in files:
        filepath = os.path.join(EXTRACTED_DIR, file)
        print(f"Loading {filepath}")
        try:
            with open(filepath, "r") as f:
                records = json.load(f)
            if not records:
                print(f"No records in {file}, skipping.")
                continue
            insert_raw_and_aggregates(records)
        except Exception as e:
            print(f"Failed to process {file}: {e}")

    print("ingestion_update finished.")