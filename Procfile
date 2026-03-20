release: python manage.py migrate
web: gunicorn quizApp.wsgi:application --bind 0.0.0.0:$PORT