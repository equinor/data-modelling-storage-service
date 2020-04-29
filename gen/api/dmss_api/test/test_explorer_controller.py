# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from dmss_api.models.document_response import DocumentResponse  # noqa: E501
from dmss_api.test import BaseTestCase


class TestExplorerController(BaseTestCase):
    """ExplorerController integration test stubs"""

    def test_add(self):
        """Test case for add

        Add document
        """
        body = None
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/explorer/{data_source_id}/add'.format(data_source_id='data_source_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove(self):
        """Test case for remove

        Remove document
        """
        body = None
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/explorer/{data_source_id}/remove'.format(data_source_id='data_source_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
