release: python manage.py migrate
web: gunicorn quiz_app.wsgi:application --bind 0.0.0.0:$PORT