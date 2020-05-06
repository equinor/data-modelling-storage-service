# dmss_api.DatasourceApi

All URIs are relative to *http://0.0.0.0:8000/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all**](DatasourceApi.md#get_all) | **GET** /data-sources | Get all data sources
[**get_data_source**](DatasourceApi.md#get_data_source) | **GET** /data-sources/{dataSourceId} | Get data source
[**save**](DatasourceApi.md#save) | **POST** /data-sources/{dataSourceId} | Add data source


# **get_all**
> list[object] get_all()

Get all data sources

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
    api_instance = dmss_api.DatasourceApi(api_client)
    
    try:
        # Get all data sources
        api_response = api_instance.get_all()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DatasourceApi->get_all: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**list[object]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of data sources |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_data_source**
> dict(str, object) get_data_source(data_source_id)

Get data source

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
    api_instance = dmss_api.DatasourceApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID

    try:
        # Get data source
        api_response = api_instance.get_data_source(data_source_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DatasourceApi->get_data_source: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 

### Return type

**dict(str, object)**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Data source |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save**
> InlineResponse200 save(data_source_id, request_body)

Add data source

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
    api_instance = dmss_api.DatasourceApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
request_body = None # dict(str, object) | Object containing all info for a document

    try:
        # Add data source
        api_response = api_instance.save(data_source_id, request_body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DatasourceApi->save: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **request_body** | [**dict(str, object)**](object.md)| Object containing all info for a document | 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

