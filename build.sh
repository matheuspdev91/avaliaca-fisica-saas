#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
export PYTHON_VERSION=3.11.9


# CRIAR SUPERUSER AUTOMATICO
python manage.py createsuperuser --noinput || true