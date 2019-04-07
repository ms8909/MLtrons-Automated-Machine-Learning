#!/bin/bash

python manage.py migrate
python manage.py update_rails_users
python manage.py sync_sequences
# /usr/local/bin/gunicorn test_django.wsgi:application --log-file=- -w 2 -b :80
python manage.py runserver 0.0.0.0:80



#set -e
#nginx -c /etc/nginx/nginx.conf
#python manage.py runserver 0.0.0.0:8000