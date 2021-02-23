#!/bin/bash
# Start virtual env.
source /var/app/venv/*/bin/activate
cd /var/app/current
# Run migrations
# Need --noinput so it executes even if it meanst overwriting.
python manage.py migrate --noinput