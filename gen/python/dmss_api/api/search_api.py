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


class SearchApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def search_entities(self, data_source_id, inline_object3, **kwargs):  # noqa: E501
        """Search for entities  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_entities(data_source_id, inline_object3, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str data_source_id: The data source ID (required)
        :param InlineObject3 inline_object3: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: dict(str, object)
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.search_entities_with_http_info(data_source_id, inline_object3, **kwargs)  # noqa: E501

    def search_entities_with_http_info(self, data_source_id, inline_object3, **kwargs):  # noqa: E501
        """Search for entities  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.search_entities_with_http_info(data_source_id, inline_object3, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str data_source_id: The data source ID (required)
        :param InlineObject3 inline_object3: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(dict(str, object), status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'data_source_id',
            'inline_object3'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method search_entities" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'data_source_id' is set
        if self.api_client.client_side_validation and ('data_source_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['data_source_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `data_source_id` when calling `search_entities`")  # noqa: E501
        # verify the required parameter 'inline_object3' is set
        if self.api_client.client_side_validation and ('inline_object3' not in local_var_params or  # noqa: E501
                                                        local_var_params['inline_object3'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `inline_object3` when calling `search_entities`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'data_source_id' in local_var_params:
            path_params['dataSourceId'] = local_var_params['data_source_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'inline_object3' in local_var_params:
            body_params = local_var_params['inline_object3']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/search/{dataSourceId}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='dict(str, object)',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
