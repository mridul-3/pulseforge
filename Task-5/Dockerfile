# Dockerfile for Prometheus exporter service
FROM python:3.11-slim

WORKDIR /app

COPY metrics.py .

RUN pip install prometheus_client flask

EXPOSE 8000

CMD ["python", "metrics.py"]