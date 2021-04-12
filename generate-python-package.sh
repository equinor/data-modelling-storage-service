#!/usr/bin/env bash

PACKAGE_VERSION=${PACKAGE_VERSION:="0.0.1"}
mkdir -p gen/dmss_api
echo "Creating DMSS Python package version $PACKAGE_VERSION"
docker run --rm \
    --network="host" \
    -v ${PWD}:/local \
    --user $(id -u):$(id -g) \
    openapitools/openapi-generator-cli generate \
    -i http://localhost:8000/openapi.json  \
    -g python \
    -o /local/gen/dmss_api \
    --additional-properties=packageName=dmss_api,packageVersion=${PACKAGE_VERSION}

