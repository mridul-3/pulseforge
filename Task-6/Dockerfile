FROM python:3.12-slim

WORKDIR /app

COPY worker.py .
COPY requirements.txt .

RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

CMD ["python", "worker.py"]