#!/bin/sh
set -euo pipefail


if [ ! -e /usr/src/app/api/home/first-run-false ] && [ "$ENVIRONMENT" = 'local' ]; then
  echo "Importing data"
  /usr/src/app/api/reset-database.sh
  touch /usr/src/app/api/home/first-run-false
fi

flask run --host=0.0.0.0
