#!/bin/bash

## Apply database migrations
#echo "Apply database migrations"
#python /code/manage.py migrate

# Start server
echo "Starting server"
python /code/manage.py runserver 0.0.0.0:8000