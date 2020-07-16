mkdir gen
docker run --rm ^
    -v %CD%:/local ^
    openapitools/openapi-generator-cli generate ^
    -i /local/openapi/api.yaml ^
    -g python-flask ^
    -o /local/gen/api ^
    --additional-properties=packageName=dmss_api,packageVersion=${API_VERSION}
