#!/bin/sh
set -eu


if [ ! -e /usr/src/app/api/home/first-run-false ] && [ "$ENVIRONMENT" = 'local' ]; then
  echo "Importing data"
  /usr/src/app/reset-database.sh
  touch /usr/src/app/api/home/first-run-false
fi

python3 /usr/src/app/app.py run
