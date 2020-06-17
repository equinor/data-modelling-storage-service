# dmss_api.BlobApi

All URIs are relative to *http://0.0.0.0:8000/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_blob_by_id**](BlobApi.md#get_blob_by_id) | **GET** /blobs/{dataSourceId}/{blobId} | Get blob by ID


# **get_blob_by_id**
> file get_blob_by_id(data_source_id, blob_id)

Get blob by ID

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
    api_instance = dmss_api.BlobApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
blob_id = 'blob_id_example' # str | The blob ID

    try:
        # Get blob by ID
        api_response = api_instance.get_blob_by_id(data_source_id, blob_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BlobApi->get_blob_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **blob_id** | **str**| The blob ID | 

### Return type

**file**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A Blob |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

