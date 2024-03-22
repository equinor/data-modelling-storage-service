#! /bin/bash
set -euo pipefail

echo "########### VERSION ##########"
if [[ -e "/code/src/version.txt" ]]; then
  cat "/code/src/version.txt"
else
  echo "No version.txt file"
fi
echo -e "########### VERSION ##########\n"


envsubst < /code/src/system_DS_template.json > /tmp/DMSS_systemDS.json

if [ "$1" = 'api' ]; then
  if [ "${RESET_DATA_SOURCE:-"on"}" == "on" ]; then
    python3 /code/src/app.py reset-app
  fi

  python3 /code/src/app.py run

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
