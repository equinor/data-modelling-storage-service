#!/usr/bin/env sh
set -eu

echo "ENVIRONMENT: $ENVIRONMENT"
export FLASK_APP="/usr/src/app/api/app_commands.py"

flask nuke-db

if [ "$ENVIRONMENT" = 'local' ]; then
    flask drop-data-sources
    echo "Importing DataSources"
    for dataSource in /usr/src/app/api/home/data_sources/"local"*.json ; do
      flask import-data-source "$dataSource"
    done
fi

sleep 5

flask init-application
