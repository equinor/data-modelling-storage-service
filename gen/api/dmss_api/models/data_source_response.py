# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from dmss_api.models.base_model_ import Model
from dmss_api import util


class DataSourceResponse(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None, type=None, document_type=None):  # noqa: E501
        """DataSourceResponse - a model defined in OpenAPI

        :param id: The id of this DataSourceResponse.  # noqa: E501
        :type id: str
        :param name: The name of this DataSourceResponse.  # noqa: E501
        :type name: str
        :param type: The type of this DataSourceResponse.  # noqa: E501
        :type type: str
        :param document_type: The document_type of this DataSourceResponse.  # noqa: E501
        :type document_type: str
        """
        self.openapi_types = {
            'id': str,
            'name': str,
            'type': str,
            'document_type': str
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'type': 'type',
            'document_type': 'documentType'
        }

        self._id = id
        self._name = name
        self._type = type
        self._document_type = document_type

    @classmethod
    def from_dict(cls, dikt) -> 'DataSourceResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DataSourceResponse of this DataSourceResponse.  # noqa: E501
        :rtype: DataSourceResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this DataSourceResponse.


        :return: The id of this DataSourceResponse.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DataSourceResponse.


        :param id: The id of this DataSourceResponse.
        :type id: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this DataSourceResponse.


        :return: The name of this DataSourceResponse.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DataSourceResponse.


        :param name: The name of this DataSourceResponse.
        :type name: str
        """

        self._name = name

    @property
    def type(self):
        """Gets the type of this DataSourceResponse.


        :return: The type of this DataSourceResponse.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this DataSourceResponse.


        :param type: The type of this DataSourceResponse.
        :type type: str
        """

        self._type = type

    @property
    def document_type(self):
        """Gets the document_type of this DataSourceResponse.


        :return: The document_type of this DataSourceResponse.
        :rtype: str
        """
        return self._document_type

    @document_type.setter
    def document_type(self, document_type):
        """Sets the document_type of this DataSourceResponse.


        :param document_type: The document_type of this DataSourceResponse.
        :type document_type: str
        """

        self._document_type = document_type
