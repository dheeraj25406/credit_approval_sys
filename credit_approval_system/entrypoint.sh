#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

echo "PostgreSQL started"

python manage.py migrate

celery -A credit_system worker -l info &

python manage.py runserver 0.0.0.0:8000