#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# RESET TEMPORÁRIO DO BANCO (IMPORTANTE)
python manage.py reset_db

# Agora sim, cria as tabelas de verdade
python manage.py migrate

# Depois coleta os estáticos
python manage.py collectstatic --noinput