# 📊 Task 0.a: Data Volume Estimation

This task estimates the total volume of time-series data generated from Fitbit-like health metrics collected continuously over time, for different participant sizes and durations.

---

## 🎯 Objective

To simulate and estimate:

- Total number of data points generated
- Estimated storage in gigabytes (raw vs. compressed)
- Infrastructure planning for large-scale ingest

---

## 📥 Assumptions

| Parameter                | Value                             |
|-------------------------|------------------------------------|
| Metrics per record      | 4 (`heart_rate`, `steps`, `distance`, `spo2`) |
| Sampling frequency      | 1 per second                       |
| Data per point          | 16 bytes (timestamp + value)       |
| Compression rate        | 80% (standard with TimescaleDB)    |
| Seconds per year        | 31,536,000                         |

---

## 📈 Output Summary

| Participants | Years | Total Data Points     | Raw Size (GB) | Compressed Size (GB) |
|--------------|-------|------------------------|---------------|-----------------------|
| 1            | 1     | 126,144,000            | 1.88          | 0.38                  |
| 1            | 5     | 630,720,000            | 9.40          | 1.88                  |
| 1,000        | 2     | 252,288,000,000        | 3,759.38      | 751.88                |
| 10,000       | 5     | 6,307,200,000,000      | 93,984.60     | 18,796.92             |

> ✅ **Note:** These numbers are critical for sizing TimescaleDB storage and compute resources when designing scalable, long-term health monitoring platforms.

---

## 🚀 Usage

```bash
cd Task-0a
python task.py
```

🧠 Insight

This script helps anticipate the data engineering footprint of continuous health monitoring platforms. With increasing number of participants or duration, the data grows exponentially — and efficient storage/compression becomes crucial.