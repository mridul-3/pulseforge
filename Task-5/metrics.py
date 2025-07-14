from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

ingestion_errors = Counter('ingestion_errors_total', 'Total ingestion errors')
ingestion_latency = Histogram('ingestion_latency_seconds', 'Time spent on ingestion')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/ingest', methods=['POST'])
@ingestion_latency.time()
def ingest():
    try:
        # simulate ingestion
        time.sleep(random.uniform(0.1, 0.3))
        if random.random() < 0.1:
            raise ValueError("Simulated ingestion failure")
        return {"status": "ok"}
    except Exception:
        ingestion_errors.inc()
        return {"status": "error"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)