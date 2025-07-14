import json
import os
import time
import psycopg2
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DB_NAME = os.getenv("POSTGRES_DB", "wearipedia")
DB_USER = os.getenv("POSTGRES_USER", "wearipedia_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "19768003")
DB_HOST = os.getenv("TSDB_HOST", "timescaledb")
DB_PORT = os.getenv("TSDB_PORT", "5432")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "wearipedia_stream")

DB_CONN = None
for i in range(10):
    try:
        DB_CONN = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
        )
        print("Connected to TimescaleDB")
        break
    except psycopg2.OperationalError as e:
        print(f"TimescaleDB connection failed (attempt {i+1}/10): {e}")
        time.sleep(5)
else:
    raise Exception("Could not connect to TimescaleDB after multiple attempts.")

consumer = None
for i in range(10):
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_BOOTSTRAP],
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id="wearipedia-group"
        )
        print(f"Connected to Kafka topic: {KAFKA_TOPIC}")
        break
    except NoBrokersAvailable:
        print(f"Kafka not ready (attempt {i+1}/10). Retrying...")
        time.sleep(5)
else:
    raise Exception("Kafka not available after multiple retries.")

def insert_to_tsdb(payload):
    try:
        with DB_CONN.cursor() as cur:
            cur.execute("""
                INSERT INTO raw_data (user_id, metric, timestamp, value)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id, metric, timestamp) DO NOTHING
            """, (
                payload["user_id"],
                payload["metric"],
                payload["timestamp"],
                payload["value"]
            ))
            DB_CONN.commit()
    except Exception as e:
        print("Failed to insert record:", e)

# Listen to Kafka and insert records
print(f"Listening to Kafka topic: {KAFKA_TOPIC}...")
for message in consumer:
    print("Received message:", message.value)
    insert_to_tsdb(message.value)
    print("Inserted into TimescaleDB.")