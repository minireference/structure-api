web: newrelic-admin run-program gunicorn --pythonpath="$PWD/struct" wsgi:application
worker: python struct/manage.py rqworker default