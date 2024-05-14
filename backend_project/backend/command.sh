#!/bin/sh
python /backend/manage.py makemigrations
python /backend/manage.py migrate
celery -A backend worker -l info &
celery -A backend beat &
python /backend/manage.py runsslserver 0.0.0.0:8000 --certificate /backend/server.crt --key /backend/server.key