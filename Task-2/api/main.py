from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import psycopg2
import os
from datetime import datetime
import logging

# Prometheus imports
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI(title="Wearipedia TimescaleDB API")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Prometheus metrics
api_requests_total = Counter(
    "api_requests_total", "Total API requests",
    ["method", "endpoint"]
)

# DB Config
DB_CONFIG = {
    "host": os.getenv("TSDB_HOST", "localhost"),
    "port": os.getenv("TSDB_PORT", "5432"),
    "dbname": os.getenv("POSTGRES_DB", "wearipedia"),
    "user": os.getenv("POSTGRES_USER", "wearipedia_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "19768003"),
}

# Define response schema
class TimeSeriesRecord(BaseModel):
    timestamp: str
    value: float

# Middleware to count API requests
@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    api_requests_total.labels(method=request.method, endpoint=request.url.path).inc()
    return response

# Route: Expose Prometheus metrics
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Helper: Choose appropriate table based on query span
def select_table(start_date: str, end_date: str) -> str:
    fmt = "%Y-%m-%d"
    start = datetime.strptime(start_date, fmt)
    end = datetime.strptime(end_date, fmt)
    span = (end - start).days
    logging.info(f"Date range span: {span} days")

    if span <= 3:
        return "raw_data"
    elif span <= 30:
        return "data_1h"
    else:
        return "data_1d"

# Main endpoint to fetch timeseries data
@app.get("/data", response_model=List[TimeSeriesRecord])
def get_data(
    user_id: str = Query(..., description="User ID, e.g. synthetic_001"),
    metric: str = Query(..., description="Metric name, e.g. heart_rate"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD"),
):
    try:
        table = select_table(start_date, end_date)
        logging.info(f"[GET /data] Querying table '{table}' for user '{user_id}', metric '{metric}'")

        query = f"""
        SELECT timestamp, value
        FROM {table}
        WHERE user_id = %s AND metric = %s
        AND timestamp BETWEEN %s AND %s
        ORDER BY timestamp;
        """

        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (user_id, metric, start_date, end_date))
                rows = cur.fetchall()

        return [{"timestamp": row[0].isoformat(), "value": float(row[1])} for row in rows]

    except Exception as e:
        logging.exception("Error in /data route")
        return {"error": str(e)}