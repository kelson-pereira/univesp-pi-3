web: gunicorn univesp_pi_3.wsgi
web: daphne -b 0.0.0.0 -p $PORT univesp_pi_3.asgi:application
worker: celery -A univesp_pi_3 worker --loglevel=info
beat: celery -A univesp_pi_3 beat --loglevel=info