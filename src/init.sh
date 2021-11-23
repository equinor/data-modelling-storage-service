#!/bin/sh
set -eu

if [ "$1" = 'api' ]; then
  if [ "${ENVIRONMENT:-'local'}" != "local" ]; then
    cat version.txt || true
    gunicorn app:create_app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000
  else
    python3 /code/app.py run
  fi
elif [ "$1" = 'reset-app' ]; then
  python3 /code/app.py reset-app
elif [ "$1" = 'create-key' ]; then
  python3 /code/app.py create-key
elif [ "$1" = 'behave' ]; then
  shift
  behave "$@"
else
  exec "$@"
fi
