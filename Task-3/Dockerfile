FROM python:3.12-slim

WORKDIR /app

COPY ingestion_update.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "ingestion_update.py"]