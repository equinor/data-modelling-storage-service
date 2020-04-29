# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from dmss_api.models.document_response import DocumentResponse  # noqa: E501
from dmss_api.test import BaseTestCase


class TestDocumentController(BaseTestCase):
    """DocumentController integration test stubs"""

    def test_get_document(self):
        """Test case for get_document

        Get document
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v2/documents/{data_source_id}/{document_id}'.format(data_source_id='data_source_id_example', document_id='document_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
