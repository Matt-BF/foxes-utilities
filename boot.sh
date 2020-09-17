#!/bin/sh
service cron start

exec gunicorn -b :3000 --workers 3 --access-logfile - --timeout 120 --graceful-timeout 120 --error-logfile - flask_app:app
