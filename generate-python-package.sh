#!/usr/bin/env bash

# DMSS must be running locally on port 5000
# Must be run from repository root, and will create folder 'gen'

PACKAGE_VERSION=${PACKAGE_VERSION:="0.0.1"}

echo "Creating DMSS Python package version $PACKAGE_VERSION"
docker run --rm \
    --network="host" \
    -v ${PWD}:/local \
    openapitools/openapi-generator-cli:v7.3.0 generate \
    -i http://localhost:5000/openapi.json  \
    -g python \
    -o /local/gen/dmss_api \
    --additional-properties=packageName=dmss_api,packageVersion=${PACKAGE_VERSION}

