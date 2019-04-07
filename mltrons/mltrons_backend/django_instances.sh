#!/bin/bash

set -e

python manage.py migrate

if [ "$APP_ENV" == "local" ]; then
   python manage.py runserver 0.0.0.0:8100
else
  if [ "$APP_ENV" == "production" ]; then
    ./hotpath-agent -server https://api.mindsight.io/query &
  fi
  gunicorn -b 0.0.0.0:8100 -t 36000 test_django.wsgi
fi
#[ "$APP_ENV" == "dev" ] && python manage.py runserver_plus 0.0.0.0:80 || gunicorn -b 0.0.0.0:80 -t 36000 test_django.wsgi
