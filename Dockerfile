FROM python:3.10-slim

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
      tesseract-ocr \
      tesseract-ocr-vie \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
