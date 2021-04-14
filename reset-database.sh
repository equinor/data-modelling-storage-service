#!/usr/bin/env sh
set -eu

echo "ENVIRONMENT: $ENVIRONMENT"
export APP_PATH="/usr/src/app/app.py"

python3 $APP_PATH nuke-db

if [ "$ENVIRONMENT" = 'local' ]; then
    python3 $APP_PATH drop-data-sources
    echo "Importing DataSources"
    for dataSource in /usr/src/app/api/home/data_sources/"local"*.json ; do
      python3 $APP_PATH import-data-source "$dataSource"
    done
fi

sleep 5

python3 $APP_PATH init-application