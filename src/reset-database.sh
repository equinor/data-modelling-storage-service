#!/usr/bin/env sh
set -eu

echo "ENVIRONMENT: $ENVIRONMENT"
export APP_PATH="/code/app.py"

python3 $APP_PATH nuke-db

if [ "$ENVIRONMENT" = 'local' ]; then
    echo "Importing DataSources"
    for dataSource in /code/home/system/data_sources/*.json ; do
      python3 $APP_PATH import-data-source "$dataSource"
    done
fi

python3 $APP_PATH init-application
