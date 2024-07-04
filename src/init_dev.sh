#!/bin/bash

set -euo pipefail
BASE_DIR=${BASE_DIR:-"/code/src"}
TMP_DIR=$1

echo "########### VERSION ##########"
if [[ -e "$BASE_DIR/version.txt" ]]; then
    cat "$BASE_DIR/version.txt"
else
    echo "No version.txt file"
fi
echo -e "########### VERSION ##########\n"

if [ -d "$BASE_DIR/storage/repository_plugins" ]; then
    echo "Checking for plugin requirements..."

    cd "$BASE_DIR/storage/repository_plugins"
    PLUGINS=$(ls)
    for plugin in $PLUGINS; do
        echo "Installing requirements for plugin $plugin"
        pip install -r "$plugin/requirements.txt"
    done

    cd -
fi

# Add debugging statements
echo "Running envsubst to generate $TMP_DIR/DMSS_systemDS.json"

envsubst < "$BASE_DIR/system_DS_template.json" > "$TMP_DIR/DMSS_systemDS.json"
if [[ -e "$TMP_DIR/DMSS_systemDS.json" ]]; then
    echo "$TMP_DIR/DMSS_systemDS.json created successfully"
    cat "$TMP_DIR/DMSS_systemDS.json"
else
    echo "Failed to create $TMP_DIR/DMSS_systemDS.json"
fi

if [ "$2" = 'api' ]; then
    if [ "${RESET_DATA_SOURCE:-"on"}" == "on" ]; then
        python "$BASE_DIR/app.py" reset_app "$TMP_DIR/DMSS_systemDS.json"
    fi
    python "$BASE_DIR/app.py" run
elif [ "$2" = 'reset-app' ]; then
    python "$BASE_DIR/app.py" reset_app "$TMP_DIR/DMSS_systemDS.json"
elif [ "$2" = 'create-key' ]; then
    python "$BASE_DIR/app.py" create_key
  elif [ "$2" = 'init_application' ]; then
    python "$BASE_DIR/app.py" init_application
elif [ "$2" = 'behave' ]; then
    shift
    cd src
    behave "$@"
else
    echo "Invalid command: $2"
fi
