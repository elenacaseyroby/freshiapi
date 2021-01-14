#!/bin/bash
# Start virtual env.
source /var/app/venv/*/bin/activate
cd /var/app/staging
# Create a staticfiles folder with all static files. 
# Need --noinput so it executes even if it meanst overwriting.
python manage.py collectstatic --noinput