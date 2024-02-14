#!/bin/bash



sleep 25

# Run Django development server
python manage.py makemigrations
python manage.py migrate

# Check if the database is empty
result=$(python manage.py shell -c "from news.models import News; count = News.objects.count(); print(count)")

if [ $result -eq 0 ]; then
    # If the database is empty, run the script to fill it
    python manage.py shell < baza_docker.py
fi

python manage.py runserver 0.0.0.0:8000
