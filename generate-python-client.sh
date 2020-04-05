#!/usr/bin/env bash

mkdir -p gen
docker run --rm \
    -v ${PWD}:/local \
    --user $(id -u):$(id -g) \
    openapitools/openapi-generator-cli generate \
    -i /local/openapi/api.yaml \
    -g python \
    -o /local/gen/python \
    --additional-properties=packageName=dmss_api,packageVersion=${API_VERSION}

