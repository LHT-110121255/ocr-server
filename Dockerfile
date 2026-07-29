FROM python:3.10-slim

RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
      libgl1 \
      libglib2.0-0 \
      libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000
ENV PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
