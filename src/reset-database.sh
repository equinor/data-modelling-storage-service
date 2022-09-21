#!/usr/bin/env sh
set -eu

echo "ENVIRONMENT: $ENVIRONMENT"
export APP_PATH="/code/src/app.py"

python3 $APP_PATH nuke-db

if [ "$ENVIRONMENT" = 'local' ]; then
    echo "Importing DataSources"
    for dataSource in /code/src/home/data_sources/"local"*.json ; do
      python3 $APP_PATH import-data-source "$dataSource"
    done
fi

python3 $APP_PATH init-application
