python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic --noinput

uvicorn opop.asgi:application --host 0.0.0.0 --port 8000 --reload