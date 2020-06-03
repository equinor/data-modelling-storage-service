# dmss_api.SearchApi

All URIs are relative to *http://0.0.0.0:8000/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**search_entities**](SearchApi.md#search_entities) | **POST** /search/{dataSourceId} | Search for entities


# **search_entities**
> dict(str, object) search_entities(data_source_id, inline_object4)

Search for entities

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
    api_instance = dmss_api.SearchApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
inline_object4 = dmss_api.InlineObject4() # InlineObject4 | 

    try:
        # Search for entities
        api_response = api_instance.search_entities(data_source_id, inline_object4)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SearchApi->search_entities: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **inline_object4** | [**InlineObject4**](InlineObject4.md)|  | 

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
**200** | Search results |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

