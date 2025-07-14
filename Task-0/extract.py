import json
import os
from typing import List, Dict
import numpy as np

try:
    import wearipedia
    from wearipedia.devices.fitbit.fitbit_charge_6 import FitbitCharge6
except ImportError:
    raise ImportError("Please install wearipedia using: pip install wearipedia")

# Constants
OUTPUT_DIR = "extracted_data"
METRICS = [
    "intraday_heart_rate",
    "intraday_spo2",
    "intraday_activity",
    "intraday_breath_rate",
    "intraday_hrv",
    "intraday_active_zone_minute"
]
USER_ID = "synthetic_001"


def ensure_output_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Using existing directory: {path}")


def extract_fitbit_data() -> Dict:
    device = FitbitCharge6(
        seed=42,
        synthetic_start_date="2024-01-01",
        synthetic_end_date="2024-01-31"
    )
    device._gen_synthetic()

    raw_data = {}
    for metric in METRICS:
        try:
            print(f"Extracting: {metric}")
            data = device.get_data(metric)
            raw_data[metric] = data
        except Exception as e:
            print(f"Warning: Failed to extract {metric}: {e}")
    return raw_data


def normalize_intraday(metric: str, raw_list: List[Dict]) -> List[Dict]:
    records = []
    for daily_entry in raw_list:
        print(f"[DEBUG] Daily Entry Keys: {list(daily_entry.keys())}")

        if "heart_rate_day" not in daily_entry:
            print(f"[WARNING] 'heart_rate_day' missing from entry: {daily_entry}")
            continue

        heart_rate_days = daily_entry["heart_rate_day"]
        if not isinstance(heart_rate_days, list):
            print(f"[WARNING] Unexpected type for heart_rate_day: {type(heart_rate_days)}")
            continue

        for day_record in heart_rate_days:
            base_date = day_record.get("dateTime", "2024-01-01")
            intraday_data = day_record.get("activities-heart-intraday", {})
            dataset = intraday_data.get("dataset", [])

            print(f"[DEBUG] Processing {len(dataset)} entries for {base_date}")

            for i, entry in enumerate(dataset):
                try:
                    timestamp = f"{base_date}T{entry['time']}"
                    value = entry["value"]

                    if hasattr(value, 'item'):
                        value = value.item()
                    else:
                        value = float(value)

                    record = {
                        "user_id": USER_ID,
                        "metric": metric,
                        "timestamp": timestamp,
                        "value": value
                    }
                    records.append(record)

                except Exception as e:
                    print(f"[DEBUG] Skipping entry due to error: {e}")
                    continue

    print(f"[DEBUG] Total records created for {metric}: {len(records)}")
    return records

def normalize_spo2(data):
    records = []
    for entry in data:
        for m in entry.get("minutes", []):
            timestamp = m["minute"]
            value = m.get("value")
            if value is not None:
                records.append({
                    "user_id": USER_ID,
                    "metric": "spo2",
                    "timestamp": timestamp,
                    "value": value
                })
    print(f"[INFO] Parsed {len(records)} records for spo2")
    return records


def normalize_breath_rate(raw_list: List[Dict]) -> List[Dict]:
    records = []
    for day_entry in raw_list:
        br_data = day_entry.get("br", [])
        for record in br_data:
            try:
                date = record.get("dateTime")
                full_summary = record.get("value", {}).get("fullSleepSummary", {})
                value = full_summary.get("breathingRate")

                if date and value is not None:
                    records.append({
                        "user_id": USER_ID,
                        "metric": "breath_rate",
                        "timestamp": f"{date}T00:00:00",
                        "value": float(value)
                    })
                else:
                    print(f"[WARNING] Missing value for breath_rate on {date}")
            except Exception as e:
                print(f"[WARNING] Skipping breath_rate entry: {e}")
                continue

    print(f"[INFO] Parsed {len(records)} records for breath_rate")
    return records


def normalize_hrv(raw_list: List[Dict]) -> List[Dict]:
    records = []
    for day_entry in raw_list:
        hrv_data = day_entry.get("hrv", [])
        for record in hrv_data:
            for minute_entry in record.get("minutes", []):
                try:
                    timestamp = minute_entry.get("minute")
                    value = minute_entry.get("value", {}).get("rmssd")

                    if timestamp and value is not None:
                        records.append({
                            "user_id": USER_ID,
                            "metric": "hrv",
                            "timestamp": timestamp,
                            "value": float(value)
                        })
                    else:
                        print(f"[WARNING] Missing value for hrv at {timestamp}")
                except Exception as e:
                    print(f"[WARNING] Skipping hrv entry: {e}")
                    continue

    print(f"[INFO] Parsed {len(records)} records for hrv")
    return records

def normalize_active_zone_minute(raw_list: List[Dict]) -> List[Dict]:
    records = []
    for day_entry in raw_list:
        azm_list = day_entry.get("activities-active-zone-minutes-intraday", [])
        for azm_day in azm_list:
            base_date = azm_day.get("dateTime", "")
            for minute_entry in azm_day.get("minutes", []):
                try:
                    minute = minute_entry.get("minute")
                    value = minute_entry.get("value", {}).get("activeZoneMinutes")

                    if base_date and minute and value is not None:
                        timestamp = f"{base_date}T{minute}"
                        records.append({
                            "user_id": USER_ID,
                            "metric": "active_zone_minute",
                            "timestamp": timestamp,
                            "value": float(value)
                        })
                    else:
                        print(f"[WARNING] Missing value for active_zone_minute at {base_date} {minute}")
                except Exception as e:
                    print(f"[WARNING] Skipping active_zone_minute entry: {e}")
                    continue

    print(f"[INFO] Parsed {len(records)} records for active_zone_minute")
    return records

def normalize_activity(raw_list: List[Dict]) -> List[Dict]:
    records = []
    for entry in raw_list:
        try:
            date = entry["dateTime"]
            value = entry["value"]

            record = {
                "user_id": USER_ID,
                "metric": "activity",
                "timestamp": f"{date}T00:00:00",
                "value": float(value)
            }
            records.append(record)
        except Exception as e:
            print(f"[WARNING] Skipping invalid activity entry: {e}")
            continue

    print(f"[INFO] Parsed {len(records)} records for activity")
    return records

def clean_json(obj):
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_json(v) for v in obj]
    elif isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, (np.floating, float)):
        return float(obj)
    return obj


def save_json(records: List[Dict], filename: str):
    with open(filename, 'w') as f:
        json.dump(records, f, indent=2)
    print(f"Saved {len(records)} records to {filename}")


def run_extraction_pipeline():
    print("--- Fitbit Synthetic Data Extraction ---")
    ensure_output_directory(OUTPUT_DIR)

    raw_data = extract_fitbit_data()
    for metric, data in raw_data.items():
        try:
            short_name = metric.replace("intraday_", "")
            parsed = []

            if metric == "intraday_heart_rate":
                parsed = normalize_intraday("heart_rate", data)
            elif metric == "intraday_spo2":
                parsed = normalize_spo2(data)
            elif metric == "intraday_activity":
                parsed = normalize_activity(data)
            elif metric == "intraday_breath_rate":
                parsed = normalize_breath_rate(data)
            elif metric == "intraday_hrv":
                parsed = normalize_hrv(data)
            elif metric == "intraday_active_zone_minute":
                parsed = normalize_active_zone_minute(data)
            else:
                print(f"[WARNING] Unknown metric {metric}. Skipping.")
                continue

            save_json(parsed, os.path.join(OUTPUT_DIR, f"{short_name}.json"))

        except Exception as e:
            print(f"[ERROR] Failed to save {metric}: {e}")

if __name__ == "__main__":
    run_extraction_pipeline()