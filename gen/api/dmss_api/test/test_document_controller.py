# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from dmss_api.test import BaseTestCase


class TestDocumentController(BaseTestCase):
    """DocumentController integration test stubs"""

    def test_get_by_id(self):
        """Test case for get_by_id

        Get document by ID
        """
        query_string = [('depth', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/documents/{data_source_id}/{document_id}'.format(data_source_id='data_source_id_example', document_id='document_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_by_path(self):
        """Test case for get_by_path

        Get document by path
        """
        query_string = [('path', 'path_example'),
                        ('depth', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/documents-by-path/{data_source_id}'.format(data_source_id='data_source_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update(self):
        """Test case for update

        Update document
        """
        request_body = None
        query_string = [('attribute', 'attribute_example')]
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/documents/{data_source_id}/{document_id}'.format(data_source_id='data_source_id_example', document_id='document_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(request_body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
