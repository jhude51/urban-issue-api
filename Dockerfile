# Stage 1: Builder
FROM python:3.12-slim AS builder

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /app

RUN python -m venv "${VIRTUAL_ENV}"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}"

WORKDIR /app

RUN groupadd --system app \
    && useradd --system --gid app --no-create-home app

COPY --from=builder /opt/venv /opt/venv

COPY --chown=app:app app ./app
COPY --chown=app:app docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

USER app

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "--chdir", "app", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--no-control-socket"]