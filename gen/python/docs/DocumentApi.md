# dmss_api.DocumentApi

All URIs are relative to *http://0.0.0.0:8000/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_by_id**](DocumentApi.md#get_by_id) | **GET** /documents/{dataSourceId}/{documentId} | Get document by ID
[**get_by_path**](DocumentApi.md#get_by_path) | **GET** /documents-by-path/{dataSourceId} | Get document by path
[**update**](DocumentApi.md#update) | **PUT** /documents/{dataSourceId}/{documentId} | Update document


# **get_by_id**
> dict(str, object) get_by_id(data_source_id, document_id, depth=depth)

Get document by ID

### Example

* Bearer (JWT) Authentication (jwt):
```python
from __future__ import print_function
import time
import dmss_api
from dmss_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://0.0.0.0:8000/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = dmss_api.Configuration(
    host = "http://0.0.0.0:8000/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): jwt
configuration = dmss_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with dmss_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.DocumentApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
document_id = 'document_id_example' # str | The document ID
depth = 56 # int | Limit nested depth of result. Default=999 (optional)

    try:
        # Get document by ID
        api_response = api_instance.get_by_id(data_source_id, document_id, depth=depth)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DocumentApi->get_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **document_id** | **str**| The document ID | 
 **depth** | **int**| Limit nested depth of result. Default&#x3D;999 | [optional] 

### Return type

**dict(str, object)**

### Authorization

[jwt](../README.md#jwt)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_by_path**
> dict(str, object) get_by_path(data_source_id, path, depth=depth)

Get document by path

### Example

* Bearer (JWT) Authentication (jwt):
```python
from __future__ import print_function
import time
import dmss_api
from dmss_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://0.0.0.0:8000/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = dmss_api.Configuration(
    host = "http://0.0.0.0:8000/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): jwt
configuration = dmss_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with dmss_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.DocumentApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
path = 'path_example' # str | The document path
depth = 56 # int | Limit nested depth of result. Default=999 (optional)

    try:
        # Get document by path
        api_response = api_instance.get_by_path(data_source_id, path, depth=depth)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DocumentApi->get_by_path: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **path** | **str**| The document path | 
 **depth** | **int**| Limit nested depth of result. Default&#x3D;999 | [optional] 

### Return type

**dict(str, object)**

### Authorization

[jwt](../README.md#jwt)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update**
> dict(str, object) update(data_source_id, document_id, request_body, attribute=attribute)

Update document

### Example

* Bearer (JWT) Authentication (jwt):
```python
from __future__ import print_function
import time
import dmss_api
from dmss_api.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://0.0.0.0:8000/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = dmss_api.Configuration(
    host = "http://0.0.0.0:8000/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): jwt
configuration = dmss_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with dmss_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.DocumentApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
document_id = 'document_id_example' # str | The document ID
request_body = None # dict(str, object) | Object containing all info for a document
attribute = 'attribute_example' # str | Path to contained document (optional)

    try:
        # Update document
        api_response = api_instance.update(data_source_id, document_id, request_body, attribute=attribute)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DocumentApi->update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **document_id** | **str**| The document ID | 
 **request_body** | [**dict(str, object)**](object.md)| Object containing all info for a document | 
 **attribute** | **str**| Path to contained document | [optional] 

### Return type

**dict(str, object)**

### Authorization

[jwt](../README.md#jwt)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The updated document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

