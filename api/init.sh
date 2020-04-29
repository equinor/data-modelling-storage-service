#!/bin/sh
set -euo pipefail

if [[ ! -v $ENVIRONMENT ]]; then
  if [ ! -e /usr/src/app/api/home/first-run-false ] && [ "$ENVIRONMENT" = 'local' ]; then
    echo "Importing data"
    /usr/src/app/api/reset-database.sh
    touch /usr/src/app/api/home/first-run-false
  fi
fi

flask run --host=0.0.0.0
