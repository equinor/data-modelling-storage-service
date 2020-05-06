# dmss_api.SearchApi

All URIs are relative to *http://0.0.0.0:8000/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**search_entities**](SearchApi.md#search_entities) | **POST** /search/{dataSourceId} | Search for entities


# **search_entities**
> dict(str, object) search_entities(data_source_id, inline_object3)

Search for entities

### Example

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


# Enter a context with an instance of the API client
with dmss_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.SearchApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
inline_object3 = dmss_api.InlineObject3() # InlineObject3 | 

    try:
        # Search for entities
        api_response = api_instance.search_entities(data_source_id, inline_object3)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SearchApi->search_entities: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **inline_object3** | [**InlineObject3**](InlineObject3.md)|  | 

### Return type

**dict(str, object)**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Search results |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

