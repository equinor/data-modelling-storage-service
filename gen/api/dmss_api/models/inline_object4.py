# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from dmss_api.models.base_model_ import Model
from dmss_api import util


class InlineObject4(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name=None, parent_id=None, description=None, document_id=None):  # noqa: E501
        """InlineObject4 - a model defined in OpenAPI

        :param name: The name of this InlineObject4.  # noqa: E501
        :type name: str
        :param parent_id: The parent_id of this InlineObject4.  # noqa: E501
        :type parent_id: str
        :param description: The description of this InlineObject4.  # noqa: E501
        :type description: str
        :param document_id: The document_id of this InlineObject4.  # noqa: E501
        :type document_id: str
        """
        self.openapi_types = {
            'name': str,
            'parent_id': str,
            'description': str,
            'document_id': str
        }

        self.attribute_map = {
            'name': 'name',
            'parent_id': 'parentId',
            'description': 'description',
            'document_id': 'documentId'
        }

        self._name = name
        self._parent_id = parent_id
        self._description = description
        self._document_id = document_id

    @classmethod
    def from_dict(cls, dikt) -> 'InlineObject4':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_object_4 of this InlineObject4.  # noqa: E501
        :rtype: InlineObject4
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this InlineObject4.


        :return: The name of this InlineObject4.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineObject4.


        :param name: The name of this InlineObject4.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def parent_id(self):
        """Gets the parent_id of this InlineObject4.


        :return: The parent_id of this InlineObject4.
        :rtype: str
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """Sets the parent_id of this InlineObject4.


        :param parent_id: The parent_id of this InlineObject4.
        :type parent_id: str
        """

        self._parent_id = parent_id

    @property
    def description(self):
        """Gets the description of this InlineObject4.


        :return: The description of this InlineObject4.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this InlineObject4.


        :param description: The description of this InlineObject4.
        :type description: str
        """

        self._description = description

    @property
    def document_id(self):
        """Gets the document_id of this InlineObject4.


        :return: The document_id of this InlineObject4.
        :rtype: str
        """
        return self._document_id

    @document_id.setter
    def document_id(self, document_id):
        """Sets the document_id of this InlineObject4.


        :param document_id: The document_id of this InlineObject4.
        :type document_id: str
        """
        if document_id is None:
            raise ValueError("Invalid value for `document_id`, must not be `None`")  # noqa: E501

        self._document_id = document_id
