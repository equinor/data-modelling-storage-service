#! /bin/bash
set -eu

echo "########### VERSION ##########"
if [[ -e "/code/src/version.txt" ]]; then
  cat "/code/src/version.txt"
else
  echo "No version.txt file"
fi
echo -e "########### VERSION ##########\n"

if [ "$1" = 'api' ]; then
  if [ "${DATA_SOURCE_FILES:-""}" != "" ]; then
    echo "$DATA_SOURCE_FILES" > /code/src/system_DS.json
  fi

  if [ "${RESET_DATA_SOURCE:-"on"}" == "on" ]; then
    python3 /code/src/app.py reset-app
  fi

  if [ "${ENVIRONMENT:-'local'}" != "local" ]; then
    cat version.txt || true
    gunicorn app:create_app --workers 4 --disable-redirect-access-to-syslog --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000
  else
    python3 /code/src/app.py run
  fi
elif [ "$1" = 'reset-app' ]; then
  python3 /code/src/app.py reset-app
elif [ "$1" = 'create-key' ]; then
  python3 /code/src/app.py create-key
elif [ "$1" = 'behave' ]; then
  shift
  cd src; behave "$@"
else
  exec "$@"
fi
