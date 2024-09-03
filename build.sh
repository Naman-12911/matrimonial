#!/bin/bash

# Build the project
echo "Building the project..."
python3.12 -m pip install -r requirements.txt
python3.12 pip install psycopg2

echo "Make Migration..."
python3.12 manage.py migrate --noinput

echo "Collect Static..."
python3.12 manage.py collectstatic --noinput 