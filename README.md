# 🌐 Wearipedia Fitbit Pipeline — Snyder Lab Challenge

Welcome to the **Wearipedia Fitbit Pipeline** — a complete, modular system designed to ingest, analyze, visualize, and monitor time-series health data inspired by real-world Fitbit usage. Built as part of the **Stanford Snyder Lab Challenge**, this project demonstrates how clinical teams can transform raw device data into meaningful insight through scalable architecture.

---

## 🎯 What's This Project About?

Imagine receiving wearable data from thousands of users every minute — heart rate, activity levels, sleep cycles, and more. How do you ingest it efficiently, query it fast, visualize it clearly, and scale it for real-time use?

**This repo answers that.** It’s built in clean layers, each task focusing on a critical piece of the puzzle — from synthetic data generation to real-time alerting and horizontal scaling.

---

## 🗂 Repository at a Glance

| Task | Folder | Description |
|------|--------|-------------|
| ✅ **Task 0** | `Task-0/` | Generates **synthetic Fitbit data** using Wearipedia. |
| ✅ **Task 1** | `Task-1/` | Ingests data into a **TimescaleDB** database. |
| ✅ **Task 2** | `Task-2/` | Exposes a **FastAPI backend** to query user metrics. |
| ✅ **Task 3** | `Task-3/` | Creates **hypertables & rollups** for better performance. |
| ✅ **Task 4** | `Task-4/` | A sleek **React dashboard** to explore trends visually. |
| ✅ **Task 5** | `Task-5/` | Adds **monitoring & alerts** using Prometheus & Alertmanager. |
| ✅ **Task 6** | `Task-6/` | Integrates **Kafka + Flink + Trino** for horizontal scaling. |

Each folder contains its own README with **detailed documentation, commands, design choices**, and visual examples.

---

## ✨ Highlights

- ⏱ **Time-Series Optimized**: Built on TimescaleDB for efficient querying.
- 🎨 **Beautiful UI**: React + Chart.js dashboard to view trends by metric, user, and time.
- 📡 **Live Monitoring**: Prometheus watches ingestion metrics and triggers alerts via SMTP.
- 🔁 **Scalable Architecture**: Kafka + Flink stream processing + Trino federation support.
- 🧪 **Synthetic Data**: Use realistic Fitbit-style data without device access.

---

## 🧭 Start Exploring

👉 Begin with [**Task 0**](./Task-0/README.md) to see how we simulate real Fitbit data.

Then follow along:

1. 🛠 [Ingest it](./Task-1/README.md) into a scalable TimescaleDB.
2. 🔎 [Query it](./Task-2/README.md) using our FastAPI service.
3. ⚙️ [Optimize it](./Task-3/README.md) with hypertables and rollups.
4. 📊 [Visualize it](./Task-4/README.md) in a modern UI.
5. 🚨 [Monitor it](./Task-5/README.md) with real-time alerting.
6. 🚀 [Scale it](./Task-6/README.md) horizontally across workers with Kafka & Flink.

---

## 🔍 Who Is This For?

Whether you're a:

- **Developer** exploring time-series systems,
- **Engineer** building full-stack pipelines,
- **Researcher** simulating clinical data,
- Or a **Data Enthusiast** learning about real-time systems...

This project is designed to be **approachable, modular, and inspiring**.

---

## 💡 Behind the Scenes

This was built as a response to the [Stanford Snyder Lab challenge](https://wearipedia.org/), aimed at improving **health data research pipelines**. We used open-source tools and modern software design principles to deliver a complete system from ingestion to alerting.

The system is designed to be **production-like**, but easily hackable for local experimentation.

---

## 📬 Contribute or Connect

If you like the project, give it a ⭐ or drop a message.

Want to contribute ideas or improvements? Dive into any task folder, raise issues, or open pull requests — we welcome them!

---

Thanks for stopping by.  
Stay curious! 🚀