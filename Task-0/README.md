# 🧪 Task-0: Synthetic Fitbit Data Extraction

## 📌 Objective

Simulate realistic time-series health data for multiple metrics using **Wearipedia**'s synthetic device simulator and export structured JSON files for downstream ingestion.

---

## 🧱 Tech Stack

- **Python 3.12**
- [**Wearipedia**](https://github.com/snyder-lab/wearipedia) (synthetic data library)
- **NumPy**, **JSON**, **Pandas** (for data normalization and export)
- CLI-based execution

---

## 📁 Directory Structure
Task-0/
├── extract.py             # Main script to generate and normalize synthetic data
├── requirements.txt       # Dependencies (wearipedia, numpy, etc.)
├── extracted_data/        # Output directory for normalized JSON files

---

## 📦 Setup

### 1. Install Python dependencies

```bash
cd Task-0
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

🛠️ How It Works

extract.py Overview
	•	Initializes FitbitCharge6 simulator with a fixed seed and date range.
	•	Fetches 6 metrics:
	•	Heart Rate
	•	SpO2
	•	HRV
	•	Breath Rate
	•	Active Zone Minutes
	•	Activity
	•	Normalization logic handles different JSON formats:
	•	Intraday datasets with timestamps per minute.
	•	Summary metrics aggregated daily or nightly.
	•	Nested structures parsed and flattened.
	•	Output format for all metrics:
    ```json
    {
        "user_id": "synthetic_001",
        "metric": "heart_rate",
        "timestamp": "2024-01-01T00:00:00",
        "value": 93.1
    }
    ```
    
📤 Output Files

All files are saved under extracted_data/ directory:
- heart_rate.json
- spo2.json
- hrv.json
- breath_rate.json
- active_zone_minute.json
- activity.json

▶️ Run Script

```bash
python extract.py
```

💡 Design Highlights
	•	Modular structure allows easy plug-in of new metrics or transformations.
	•	Robustness: Warnings and type checks ensure graceful failure for missing fields.
	•	Reproducibility: Fixed seed ensures consistent data for testing and benchmarking.

⸻

✅ Use Case

This module is a prerequisite for Task-1 (Ingestion) and all subsequent modules that consume Fitbit data.

⸻

🧠 Design Decisions
	•	Flat JSON structure simplifies ingestion into TimescaleDB and avoids complex joins in querying.
	•	Split normalization functions per metric to account for unique structures returned by the simulator.
	•	Only necessary fields (timestamp, value, metric, user_id) are retained to keep payload size small.