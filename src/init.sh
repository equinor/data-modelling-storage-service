#!/bin/sh
set -eu

ENVIRON=${ENVIRONMENT:="production"}
if [ ! -e /code/home/first-run-false ] && [ "$ENVIRON" = 'local' ]; then
  echo "Importing data"
  /code/reset-database.sh
  touch /code/home/first-run-false
fi

python3 /code/app.py run
