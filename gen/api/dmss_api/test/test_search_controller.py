# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from dmss_api.models.inline_object5 import InlineObject5  # noqa: E501
from dmss_api.test import BaseTestCase


class TestSearchController(BaseTestCase):
    """SearchController integration test stubs"""

    def test_search_entities(self):
        """Test case for search_entities

        Search for entities
        """
        inline_object5 = {}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/search/{data_source_id}'.format(data_source_id='data_source_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(inline_object5),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
