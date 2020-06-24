# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from dmss_api.test import BaseTestCase


class TestPackageController(BaseTestCase):
    """PackageController integration test stubs"""

    def test_find_by_name(self):
        """Test case for find_by_name

        Query packages
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/packages/{data_source_id}/findByName/{name}'.format(data_source_id='data_source_id_example', name='name_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get(self):
        """Test case for get

        Get packages
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/packages/{data_source_id}'.format(data_source_id='data_source_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
