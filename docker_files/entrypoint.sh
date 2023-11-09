#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python /code/manage.py migrate

# Create superuser
echo "Create superuser"
export DJANGO_SUPERUSER_USERNAME
export DJANGO_SUPERUSER_EMAIL
export DJANGO_SUPERUSER_PASSWORD
python /code/manage.py createsuperuser --noinput

# Start server
echo "Starting server"
python /code/manage.py runserver 0.0.0.0:8000