# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from dmss_api.test import BaseTestCase


class TestBlobController(BaseTestCase):
    """BlobController integration test stubs"""

    def test_get_blob_by_id(self):
        """Test case for get_blob_by_id

        Get blob by ID
        """
        headers = { 
            'Accept': 'application/octet-stream',
        }
        response = self.client.open(
            '/api/v1/blobs/{data_source_id}/{blob_id}'.format(data_source_id='data_source_id_example', blob_id='blob_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
