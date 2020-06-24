# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from dmss_api.models.inline_object import InlineObject  # noqa: E501
from dmss_api.models.inline_object2 import InlineObject2  # noqa: E501
from dmss_api.models.inline_object3 import InlineObject3  # noqa: E501
from dmss_api.models.inline_object4 import InlineObject4  # noqa: E501
from dmss_api.models.inline_response2001 import InlineResponse2001  # noqa: E501
from dmss_api.test import BaseTestCase


class TestExplorerController(BaseTestCase):
    """ExplorerController integration test stubs"""

    def test_add_document(self):
        """Test case for add_document

        Add document
        """
        request_body = None
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/explorer/{data_source_id}/add-document'.format(data_source_id='data_source_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(request_body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_package(self):
        """Test case for add_package

        Add package
        """
        request_body = None
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/explorer/{data_source_id}/add-package'.format(data_source_id='data_source_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(request_body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_raw(self):
        """Test case for add_raw

        Add raw document
        """
        request_body = None
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/explorer/{data_source_id}/add-raw'.format(data_source_id='data_source_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(request_body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_to_parent(self):
        """Test case for add_to_parent

        Add document to parent
        """
        inline_object = {}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/explorer/{data_source_id}/add-to-parent'.format(data_source_id='data_source_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(inline_object),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_add_to_path(self):
        """Test case for add_to_path

        Add document to path
        """
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data',
        }
        data = dict(directory='directory_example',
                    document='document_example',
                    files=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/api/v1/explorer/{data_source_id}/add-to-path'.format(data_source_id='data_source_id_example'),
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_move(self):
        """Test case for move

        Move document
        """
        request_body = None
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/explorer/{data_source_id}/move'.format(data_source_id='data_source_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(request_body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove(self):
        """Test case for remove

        Remove document
        """
        inline_object2 = {}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/explorer/{data_source_id}/remove'.format(data_source_id='data_source_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(inline_object2),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove_by_path(self):
        """Test case for remove_by_path

        Remove document by path
        """
        inline_object3 = {}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/explorer/{data_source_id}/remove-by-path'.format(data_source_id='data_source_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(inline_object3),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rename(self):
        """Test case for rename

        Rename document
        """
        inline_object4 = {}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/explorer/{data_source_id}/rename'.format(data_source_id='data_source_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(inline_object4),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
