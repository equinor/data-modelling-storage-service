# coding: utf-8

"""
    Data Modelling Storage Service API

    Data storage service for DMT  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from dmss_api.api_client import ApiClient
from dmss_api.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class BlobApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_blob_by_id(self, data_source_id, blob_id, **kwargs):  # noqa: E501
        """Get blob by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_blob_by_id(data_source_id, blob_id, async_req=True)
        >>> result = thread.get()

        :param data_source_id: The data source ID (required)
        :type data_source_id: str
        :param blob_id: The blob ID (required)
        :type blob_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: file
        """
        kwargs['_return_http_data_only'] = True
        return self.get_blob_by_id_with_http_info(data_source_id, blob_id, **kwargs)  # noqa: E501

    def get_blob_by_id_with_http_info(self, data_source_id, blob_id, **kwargs):  # noqa: E501
        """Get blob by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_blob_by_id_with_http_info(data_source_id, blob_id, async_req=True)
        >>> result = thread.get()

        :param data_source_id: The data source ID (required)
        :type data_source_id: str
        :param blob_id: The blob ID (required)
        :type blob_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(file, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'data_source_id',
            'blob_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_blob_by_id" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'data_source_id' is set
        if self.api_client.client_side_validation and ('data_source_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['data_source_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `data_source_id` when calling `get_blob_by_id`")  # noqa: E501
        # verify the required parameter 'blob_id' is set
        if self.api_client.client_side_validation and ('blob_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['blob_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `blob_id` when calling `get_blob_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'data_source_id' in local_var_params:
            path_params['dataSourceId'] = local_var_params['data_source_id']  # noqa: E501
        if 'blob_id' in local_var_params:
            path_params['blobId'] = local_var_params['blob_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/octet-stream'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/blobs/{dataSourceId}/{blobId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))
