# 🌐 Task-2: FastAPI Backend for Fitbit Time Series Data

## 📌 Objective

Build a lightweight **FastAPI** service to expose RESTful endpoints for accessing Fitbit health metrics stored in **TimescaleDB**. Supports dynamic table selection based on query span (raw, 1-hour, 1-day).

---

## 🧱 Tech Stack

- **FastAPI** + **Uvicorn**
- **TimescaleDB** (via PostgreSQL)
- **Psycopg2** for database access
- **Pydantic** for data validation
- **Docker** for containerized deployment

---

## 📁 Directory Structure
Task-2/
├── api/
│   ├── main.py            # FastAPI app
│   └── requirements.txt   # FastAPI, psycopg2, pydantic
├── Dockerfile             # API container

---

## ⚙️ API Features

### `GET /data`

Fetch time series values based on user, metric, and date range.

#### Query Parameters

| Param       | Type   | Example             | Description                       |
|-------------|--------|---------------------|-----------------------------------|
| `user_id`   | string | `synthetic_001`     | Unique user ID                    |
| `metric`    | string | `heart_rate`        | Metric name (e.g., spo2, hrv)     |
| `start_date`| string | `2024-01-01`        | Start date (YYYY-MM-DD)          |
| `end_date`  | string | `2024-01-03`        | End date (YYYY-MM-DD)            |

#### Example Request
```bash
curl "http://localhost:8000/data?user_id=synthetic_001&metric=heart_rate&start_date=2024-01-01&end_date=2024-01-03"
``` 
📊 Table Selection Logic

The app chooses the table dynamically based on the date span:
- **Raw Data**: If the date span is less than 1 day.
- **1-Hour Aggregated**: If the span is between 1 day and 7 days.
- **1-Day Aggregated**: If the span is more than 7 days.
### Example Response
```json
[
    {
        "user_id": "synthetic_001",
        "metric": "heart_rate",
        "timestamp": "2024-01-01T00:00:00",
        "value": 88.2
    },
    {
        "user_id": "synthetic_001",
        "metric": "heart_rate",
        "timestamp": "2024-01-01T01:00:00",
        "value": 90.1
    }
]
```

🐳 Docker Support

Build the API image
```bash
docker-compose build api
```
Run the API service
```bash
docker-compose up -d api
```

The API will be accessible at:
📍 http://localhost:8000/data

🔄 CORS Support

CORS middleware is enabled to allow requests from any frontend domain (e.g., React).

⸻

🧠 Design Decisions
	• Dynamic routing using Pydantic + FastAPI’s dependency injection model.
	• Time-aware logic selects optimal aggregation table to scale queries.
	• Clean separation of logic, environment config, and schema for maintainability.
	• Query results are always returned sorted by timestamp for chart rendering.

⸻

🧪 Testing

You can test the API with:
```bash
curl "http://localhost:8000/data?user_id=synthetic_001&metric=activity&start_date=2024-01-01&end_date=2024-01-03"
```
Or using Swagger UI at:
🔗 http://localhost:8000/docs