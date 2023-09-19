#!/bin/sh

if [ "$DATABASE" = "postgres" ]
 then
   echo "Waiting for Postgres..."

   while ! nc -z "$DB_HOST" "$DB_PORT" ; do
       sleep 0.1
   done
   echo "PostgreSQl started"
fi

python manage.py collectstatic --no-input
#python manage.py flush --no-input
python manage.py migrate

exec "$@"