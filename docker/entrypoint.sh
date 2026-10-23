#!/bin/bash
set -e

echo "Applying database migrations..."
python app/manage.py migrate --noinput

echo "Starting application..."
exec "$@"