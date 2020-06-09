# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from dmss_api.models.inline_response200 import InlineResponse200  # noqa: E501
from dmss_api.test import BaseTestCase


class TestDatasourceController(BaseTestCase):
    """DatasourceController integration test stubs"""

    def test_get_all(self):
        """Test case for get_all

        Get all data sources
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/data-sources',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_data_source(self):
        """Test case for get_data_source

        Get data source
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/data-sources/{data_source_id}'.format(data_source_id='data_source_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_save(self):
        """Test case for save

        Add data source
        """
        request_body = None
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/data-sources/{data_source_id}'.format(data_source_id='data_source_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(request_body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
