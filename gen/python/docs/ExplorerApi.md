# dmss_api.ExplorerApi

All URIs are relative to *http://0.0.0.0:8000/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_document**](ExplorerApi.md#add_document) | **POST** /explorer/{dataSourceId}/add-document | Add document
[**add_package**](ExplorerApi.md#add_package) | **POST** /explorer/{dataSourceId}/add-package | Add package
[**add_raw**](ExplorerApi.md#add_raw) | **POST** /explorer/{dataSourceId}/add-raw | Add raw document
[**add_to_parent**](ExplorerApi.md#add_to_parent) | **POST** /explorer/{dataSourceId}/add-to-parent | Add document to parent
[**add_to_path**](ExplorerApi.md#add_to_path) | **POST** /explorer/{dataSourceId}/add-to-path | Add document to path
[**move**](ExplorerApi.md#move) | **PUT** /explorer/{dataSourceId}/move | Move document
[**remove**](ExplorerApi.md#remove) | **POST** /explorer/{dataSourceId}/remove | Remove document
[**rename**](ExplorerApi.md#rename) | **PUT** /explorer/{dataSourceId}/rename | Rename document


# **add_document**
> str add_document(data_source_id, request_body)

Add document

### Example

```python
from __future__ import print_function
import time
import dmss_api
from dmss_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with dmss_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.ExplorerApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
request_body = None # dict(str, object) | Object containing all info for a document

    try:
        # Add document
        api_response = api_instance.add_document(data_source_id, request_body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExplorerApi->add_document: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **request_body** | [**dict(str, object)**](object.md)| Object containing all info for a document | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Added document UID |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_package**
> dict(str, object) add_package(data_source_id, request_body)

Add package

### Example

```python
from __future__ import print_function
import time
import dmss_api
from dmss_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with dmss_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.ExplorerApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
request_body = None # dict(str, object) | Object containing all info for a document

    try:
        # Add package
        api_response = api_instance.add_package(data_source_id, request_body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExplorerApi->add_package: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **request_body** | [**dict(str, object)**](object.md)| Object containing all info for a document | 

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
**200** | Added package |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_raw**
> str add_raw(data_source_id, request_body)

Add raw document

### Example

```python
from __future__ import print_function
import time
import dmss_api
from dmss_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with dmss_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.ExplorerApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
request_body = None # dict(str, object) | Object containing all info for a document

    try:
        # Add raw document
        api_response = api_instance.add_raw(data_source_id, request_body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExplorerApi->add_raw: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **request_body** | [**dict(str, object)**](object.md)| Object containing all info for a document | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Added document UID |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_to_parent**
> InlineResponse2001 add_to_parent(data_source_id, inline_object)

Add document to parent

### Example

```python
from __future__ import print_function
import time
import dmss_api
from dmss_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with dmss_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.ExplorerApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
inline_object = dmss_api.InlineObject() # InlineObject | 

    try:
        # Add document to parent
        api_response = api_instance.add_to_parent(data_source_id, inline_object)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExplorerApi->add_to_parent: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **inline_object** | [**InlineObject**](InlineObject.md)|  | 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The UID of the added document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_to_path**
> dict(str, object) add_to_path(data_source_id, request_body)

Add document to path

### Example

```python
from __future__ import print_function
import time
import dmss_api
from dmss_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with dmss_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.ExplorerApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
request_body = None # dict(str, object) | Object containing all info for a document

    try:
        # Add document to path
        api_response = api_instance.add_to_path(data_source_id, request_body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExplorerApi->add_to_path: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **request_body** | [**dict(str, object)**](object.md)| Object containing all info for a document | 

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
**200** | Added document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **move**
> dict(str, object) move(data_source_id, request_body)

Move document

### Example

```python
from __future__ import print_function
import time
import dmss_api
from dmss_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with dmss_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.ExplorerApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
request_body = None # dict(str, object) | Object containing all info for a document

    try:
        # Move document
        api_response = api_instance.move(data_source_id, request_body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExplorerApi->move: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **request_body** | [**dict(str, object)**](object.md)| Object containing all info for a document | 

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
**200** | Added document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove**
> object remove(data_source_id, inline_object1)

Remove document

### Example

```python
from __future__ import print_function
import time
import dmss_api
from dmss_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with dmss_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.ExplorerApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
inline_object1 = dmss_api.InlineObject1() # InlineObject1 | 

    try:
        # Remove document
        api_response = api_instance.remove(data_source_id, inline_object1)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExplorerApi->remove: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **inline_object1** | [**InlineObject1**](InlineObject1.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Remove status |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **rename**
> dict(str, object) rename(data_source_id, inline_object2)

Rename document

### Example

```python
from __future__ import print_function
import time
import dmss_api
from dmss_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with dmss_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = dmss_api.ExplorerApi(api_client)
    data_source_id = 'data_source_id_example' # str | The data source ID
inline_object2 = dmss_api.InlineObject2() # InlineObject2 | 

    try:
        # Rename document
        api_response = api_instance.rename(data_source_id, inline_object2)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ExplorerApi->rename: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| The data source ID | 
 **inline_object2** | [**InlineObject2**](InlineObject2.md)|  | 

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
**200** | Added document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
