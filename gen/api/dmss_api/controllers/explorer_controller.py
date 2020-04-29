import connexion
import six

from dmss_api.models.inline_object import InlineObject  # noqa: E501
from dmss_api.models.inline_object1 import InlineObject1  # noqa: E501
from dmss_api.models.inline_object2 import InlineObject2  # noqa: E501
from dmss_api.models.inline_response2001 import InlineResponse2001  # noqa: E501
from dmss_api import util


def add_package(data_source_id, request_body):  # noqa: E501
    """Add package

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param request_body: Object containing all info for a document
    :type request_body: dict | bytes

    :rtype: Dict[str, object]
    """
    return 'do some magic!'


def add_raw(data_source_id, request_body):  # noqa: E501
    """Add raw document

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param request_body: Object containing all info for a document
    :type request_body: dict | bytes

    :rtype: str
    """
    return 'do some magic!'


def add_to_parent(data_source_id, inline_object):  # noqa: E501
    """Add document to parent

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param inline_object: 
    :type inline_object: dict | bytes

    :rtype: InlineResponse2001
    """
    if connexion.request.is_json:
        inline_object = InlineObject.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def add_to_path(data_source_id, request_body):  # noqa: E501
    """Add document to path

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param request_body: Object containing all info for a document
    :type request_body: dict | bytes

    :rtype: Dict[str, object]
    """
    return 'do some magic!'


def move(data_source_id, request_body):  # noqa: E501
    """Move document

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param request_body: Object containing all info for a document
    :type request_body: dict | bytes

    :rtype: Dict[str, object]
    """
    return 'do some magic!'


def remove(data_source_id, inline_object1):  # noqa: E501
    """Remove document

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param inline_object1: 
    :type inline_object1: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        inline_object1 = InlineObject1.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def rename(data_source_id, inline_object2):  # noqa: E501
    """Rename document

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param inline_object2: 
    :type inline_object2: dict | bytes

    :rtype: Dict[str, object]
    """
    if connexion.request.is_json:
        inline_object2 = InlineObject2.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
