# 📦 Task-3: Hypertable Optimization with TimescaleDB

## 📌 Objective

Optimize query performance for large-scale Fitbit time series data by creating **hypertables** and **continuous aggregates** using **TimescaleDB**.  
This enables efficient storage, indexing, and aggregation over time at multiple resolutions (1-minute, 1-hour, 1-day).

---

## 🧱 Tech Stack

- **PostgreSQL** + **TimescaleDB**
- **Python** for ingestion script
- **Docker** for orchestration

---

## 📁 Directory Structure
```Task-3/
├── hypertables.sql          # SQL to create hypertables and aggregates
├── ingestion_update.py      # Python script to insert raw + rollup into aggregates
├── requirements.txt         # psycopg2, pandas, python-dotenv
├── Dockerfile               # Docker container for ingestion_update
```
---

## 🛠️ Hypertable Setup

### File: `hypertables.sql`

Creates the following tables:

- `raw_data` – Primary hypertable
- `data_1m` – Aggregated view (1-minute)
- `data_1h` – Aggregated view (1-hour)
- `data_1d` – Aggregated view (1-day)

> All aggregates include `avg(value)` over time per `user_id` and `metric`.

### Run once inside TimescaleDB container:

```bash
docker cp Task-3/hypertables.sql timescaledb:/hypertables.sql
docker exec -it timescaledb psql -U wearipedia_user -d wearipedia -f /hypertables.sql

```

🚀 Aggregated Ingestion Pipeline

File: ingestion_update.py
	• Loads each metric JSON file from extracted_data/
	• Inserts data into raw_data
	• Computes aggregates in Python (pandas) and inserts into:
	• data_1m
	• data_1h
	• data_1d

🧠 Design Decisions
	• Used pandas for performant grouping and mean aggregation.
	• Ingestion script is modular and robust against file errors.
	• JSON data is dynamically read and automatically routed to the correct hypertable and aggregate.
	• Continuous aggregates enable API to dynamically query appropriate granularity (used in Task-2).