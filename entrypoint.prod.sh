#!/bin/sh
python3 manage.py migrate        # Apply database migrations
python3 manage.py collectstatic --noinput  # collect static files
# Prepare log files and start outputting logs to stdout
touch /home/app/logs/gunicorn.log
touch /home/app/logs/access.log
tail -n 0 -f /home/app/logs/*.log &
# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn savanah.wsgi:application \
    --name savannah \
    --bind unix:savanah.sock \
    --workers 3 \
    --log-level=info \
    --log-file=/home/app/logs/gunicorn.log \
    --access-logfile=/home/app/logs/access.log &

echo Starting nginx
exec service nginx start \
    "$@"


