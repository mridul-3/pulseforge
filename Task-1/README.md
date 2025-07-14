# 🧩 Task-1: Ingestion Pipeline

## 📌 Objective

Develop a containerized ingestion pipeline to load synthetic Fitbit JSON data (from Task-0) into a **TimescaleDB** instance. This pipeline ensures clean ingestion, idempotency, and is driven by environment configurations for flexibility across environments.

---

## 🧱 Tech Stack

- **Python 3.12**
- **TimescaleDB 2.x** (on PostgreSQL 14)
- **Docker** & **Docker Compose**
- `psycopg2` for PostgreSQL interaction
- Flat JSON-based data format

---

## 📁 Directory Structure
Task-1/
├── ingest.py
├── Dockerfile
├── requirements.txt

---

## ⚙️ Functionality Overview

1. **Reads** Fitbit `.json` files from the mounted directory (`./Task-0/extracted_data`).
2. **Validates** and parses metric-wise data records.
3. **Inserts** them into a TimescaleDB hypertable named `raw_data`.
4. Ensures **idempotency** using `ON CONFLICT DO NOTHING`.

### Example Data Format:

```json
{
  "user_id": "synthetic_001",
  "metric": "heart_rate",
  "timestamp": "2024-01-01T00:00:00",
  "value": 88.2
}

✅ Supported Metrics

As of Task-1, we support ingesting:
	•	heart_rate
	•	spo2
	•	activity
	•	hrv
	•	breath_rate
	•	active_zone_minute

These are validated for uniform flat schema:
    {
    "user_id": "synthetic_001",
    "metric": "heart_rate",
    "timestamp": "2024-01-01T00:00:00",
    "value": 93.1
    }

📦 Docker Integration

A lightweight Dockerfile is used to containerize the ingestion logic.

🧪 How to Run

Ensure you have TimescaleDB running first:
```bash
docker-compose up -d timescaledb
```

Then build and run the ingestion service:
```bash
docker-compose build ingestion
docker-compose run --rm ingestion
```


🔍 Design Decisions
	•	Decoupled Schema Handling: Flat schema assumption in Task-0 ensures ingestion logic in Task-1 stays clean and minimal.
	•	Idempotent Writes: ON CONFLICT DO NOTHING avoids duplicate inserts on reruns.
	•	Environment-driven Config: Database creds and port are pulled from .env, making this safe for production Docker orchestration.

🧼 Code Quality
	•	Single-responsibility principle followed in ingest.py (modular methods: connect_db, insert_records, etc.)
	•	Logging included for clear visibility.
	•	Safe JSON parsing with validation.

📎 Notes
	•	This task assumes the JSON format output from Task-0 is already normalized.
	•	If you rerun Task-0, ensure you rerun Task-1 to reinsert updated files.
