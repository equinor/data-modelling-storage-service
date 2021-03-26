#!/bin/sh
set -eu

ENVIRON=${ENVIRONMENT:="production"}
if [ ! -e /usr/src/app/api/home/first-run-false ] && [ "$ENVIRON" = 'local' ]; then
  echo "Importing data"
  /usr/src/app/reset-database.sh
  touch /usr/src/app/api/home/first-run-false
fi

python3 /usr/src/app/app.py run
