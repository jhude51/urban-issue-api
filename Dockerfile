# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["gunicorn", "app.core.wsgi:application", "--bind", "0.0.0.0:8000"]