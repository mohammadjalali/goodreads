#!/bin/sh

python ../src/goodreads/manage.py loaddata ../src/goodreads/user/fixtures/user.json
python ../src/goodreads/manage.py loaddata ../src/goodreads/book/fixtures/*.json
