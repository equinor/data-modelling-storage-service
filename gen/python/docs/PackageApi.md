# dmss_api.PackageApi

All URIs are relative to *http://0.0.0.0:8000/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find_by_name**](PackageApi.md#find_by_name) | **GET** /packages/{dataSourceId}/findByName/{name} | Query packages
[**get**](PackageApi.md#get) | **GET** /packages/{dataSourceId} | Get packages


# **find_by_name**
> object find_by_name(data_source_id, name)

Query packages

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
    api_instance = dmss_api.PackageApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
name = 'name_example' # str | The name of the package to find

    try:
        # Query packages
        api_response = api_instance.find_by_name(data_source_id, name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PackageApi->find_by_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **name** | **str**| The name of the package to find | 

### Return type

**object**

### Authorization

[jwt](../README.md#jwt)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Package |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get**
> list[object] get(data_source_id)

Get packages

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
    api_instance = dmss_api.PackageApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID

    try:
        # Get packages
        api_response = api_instance.get(data_source_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PackageApi->get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 

### Return type

**list[object]**

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

