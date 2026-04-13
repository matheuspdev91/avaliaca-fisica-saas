#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Cria pastas de estáticos se não existirem
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images

# Coleta arquivos estáticos
python manage.py collectstatic --no-input

# Roda migrações
python manage.py migrate