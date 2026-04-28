#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput



# CRIAR SUPERUSER AUTOMATICO
python manage.py createsuperuser \
  --noinput \
  --username admin \
  --email admin@email.com || true

  DJANGO_SUPERUSER_PASSWORD=123456


# SEED.PY

seed_exercicios.py  →  seed.py