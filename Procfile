release: python manage.py migrate --noinput
web: newrelic-admin run-program gunicorn parkalerts.wsgi --log-file - --workers 3 -k gevent --worker-connections 100 --config gunicorn_config.py
