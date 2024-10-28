#!/bin/sh

python src/goodreads/manage.py migrate

exec "$@"
