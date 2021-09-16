#!/bin/sh
set -eu

if [ "$1" = 'api' ]; then
  python3 /code/app.py run
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
