#!/bin/bash
# Startup script for Render deployment
# This ensures migrations run before starting the server

set -e

echo "=== Starting StudyMate Backend ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"

echo "Running database migrations..."
cd /opt/render/project/src/server || cd server
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-10000}
