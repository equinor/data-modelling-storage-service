# dmss-api
Data storage service for DMT

This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 0.1.0
- Package version: 
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import dmss_api
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import dmss_api
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import dmss_api
from dmss_api.rest import ApiException
from pprint import pprint


# Defining host is optional and default to http://0.0.0.0:8000/api/v1
configuration.host = "http://0.0.0.0:8000/api/v1"
# Enter a context with an instance of the API client
with dmss_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.DatasourceApi(api_client)
    
    try:
        # Get all data sources
        api_response = api_instance.get_all()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DatasourceApi->get_all: %s\n" % e)
    
```

## Documentation for API Endpoints

All URIs are relative to *http://0.0.0.0:8000/api/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*DatasourceApi* | [**get_all**](docs/DatasourceApi.md#get_all) | **GET** /data-sources | Get all data sources
*DatasourceApi* | [**get_data_source**](docs/DatasourceApi.md#get_data_source) | **GET** /data-sources/{dataSourceId} | Get data source
*DatasourceApi* | [**save**](docs/DatasourceApi.md#save) | **POST** /data-sources/{dataSourceId} | Add data source
*DocumentApi* | [**get_by_id**](docs/DocumentApi.md#get_by_id) | **GET** /documents/{dataSourceId}/{documentId} | Get document by ID
*DocumentApi* | [**get_by_path**](docs/DocumentApi.md#get_by_path) | **GET** /documents-by-path/{dataSourceId} | Get document by path
*DocumentApi* | [**update**](docs/DocumentApi.md#update) | **PUT** /documents/{dataSourceId}/{documentId} | Update document
*ExplorerApi* | [**add_document**](docs/ExplorerApi.md#add_document) | **POST** /explorer/{dataSourceId}/add-document | Add document
*ExplorerApi* | [**add_package**](docs/ExplorerApi.md#add_package) | **POST** /explorer/{dataSourceId}/add-package | Add package
*ExplorerApi* | [**add_raw**](docs/ExplorerApi.md#add_raw) | **POST** /explorer/{dataSourceId}/add-raw | Add raw document
*ExplorerApi* | [**add_to_parent**](docs/ExplorerApi.md#add_to_parent) | **POST** /explorer/{dataSourceId}/add-to-parent | Add document to parent
*ExplorerApi* | [**add_to_path**](docs/ExplorerApi.md#add_to_path) | **POST** /explorer/{dataSourceId}/add-to-path | Add document to path
*ExplorerApi* | [**move**](docs/ExplorerApi.md#move) | **PUT** /explorer/{dataSourceId}/move | Move document
*ExplorerApi* | [**remove**](docs/ExplorerApi.md#remove) | **POST** /explorer/{dataSourceId}/remove | Remove document
*ExplorerApi* | [**rename**](docs/ExplorerApi.md#rename) | **PUT** /explorer/{dataSourceId}/rename | Rename document
*PackageApi* | [**find_by_name**](docs/PackageApi.md#find_by_name) | **GET** /packages/{dataSourceId}/findByName/{name} | Query packages
*PackageApi* | [**get**](docs/PackageApi.md#get) | **GET** /packages/{dataSourceId} | Get packages
*SearchApi* | [**search_entities**](docs/SearchApi.md#search_entities) | **POST** /search/{dataSourceId} | Search for entities


## Documentation For Models

 - [InlineObject](docs/InlineObject.md)
 - [InlineObject1](docs/InlineObject1.md)
 - [InlineObject2](docs/InlineObject2.md)
 - [InlineObject3](docs/InlineObject3.md)
 - [InlineResponse200](docs/InlineResponse200.md)
 - [InlineResponse2001](docs/InlineResponse2001.md)


## Documentation For Authorization

 All endpoints do not require authorization.

## Author



