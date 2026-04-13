#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Cria a pasta static no caminho correto do Render
mkdir -p /opt/render/project/src/static/css
mkdir -p /opt/render/project/src/static/js
mkdir -p /opt/render/project/src/static/images

python manage.py collectstatic --no-input
python manage.py migrate