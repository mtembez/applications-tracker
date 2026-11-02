# Production Multi-Stage Container for Applications Tracker
FROM python:3.13-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.13-slim AS runner

WORKDIR /app

ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    APP_TRACKER_DB=/app/data/applications.db \
    PORT=8765

RUN mkdir -p /app/data

COPY --from=builder /root/.local /root/.local
COPY . /app

EXPOSE 8765

CMD ["python3", "-m", "tracker.server"]
