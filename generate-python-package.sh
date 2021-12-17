#!/usr/bin/env bash

PACKAGE_VERSION=${PACKAGE_VERSION:="0.0.1"}

echo "Creating DMSS Python package version $PACKAGE_VERSION"
docker run --rm \
    --network="host" \
    -v ${PWD}:/local \
    openapitools/openapi-generator-cli:v5.2.1 generate \
    -i http://localhost:8000/openapi.json  \
    -g python \
    -o /local/gen/dmss_api \
    --additional-properties=packageName=dmss_api,packageVersion=${PACKAGE_VERSION}

