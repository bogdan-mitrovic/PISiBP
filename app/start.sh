#!/bin/bash


sleep 3

# Run Django development server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

