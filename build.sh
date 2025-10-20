#!/bin/bash
# Actualiza pip
pip install --upgrade pip
# Instala dependencias
pip install -r requirements.txt
# Ejecuta migraciones
python manage.py migrate
# Recopila archivos estáticos (si los tienes)
python manage.py collectstatic --noinput
