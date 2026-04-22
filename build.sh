#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py reset_db
python manage.py migrate
python manage.py collectstatic --noinput