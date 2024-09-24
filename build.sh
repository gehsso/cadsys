#!/bin/bash

echo "Starting build script"
pip install -r requirements.txt
# make migrations
#python manage.py makemigrations
#python manage.py migrate
# collectstatic
python3 manage.py collectstatic
echo "Build script completed"