release: python manage.py migrate --noinput
web: gunicorn config.wsgi:application
worker: celery worker --app=config.celery_app --loglevel=info
beat: celery beat --app=config.celery_app --loglevel=info
