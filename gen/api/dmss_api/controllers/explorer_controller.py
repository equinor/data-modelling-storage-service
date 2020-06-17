import connexion
import six

from dmss_api.models.inline_object import InlineObject  # noqa: E501
from dmss_api.models.inline_object2 import InlineObject2  # noqa: E501
from dmss_api.models.inline_object3 import InlineObject3  # noqa: E501
from dmss_api.models.inline_object4 import InlineObject4  # noqa: E501
from dmss_api.models.inline_response2001 import InlineResponse2001  # noqa: E501
from dmss_api import util


def add_document(data_source_id, request_body):  # noqa: E501
    """Add document

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param request_body: Object containing all info for a document
    :type request_body: Dict[str, ]

    :rtype: str
    """
    return 'do some magic!'


def add_package(data_source_id, request_body):  # noqa: E501
    """Add package

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param request_body: Object containing all info for a document
    :type request_body: Dict[str, ]

    :rtype: Dict[str, object]
    """
    return 'do some magic!'


def add_raw(data_source_id, request_body):  # noqa: E501
    """Add raw document

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param request_body: Object containing all info for a document
    :type request_body: Dict[str, ]

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


def add_to_path(data_source_id, directory=None, document=None, files=None):  # noqa: E501
    """Add document to path

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param directory: 
    :type directory: str
    :param document: 
    :type document: str
    :param files: 
    :type files: List[str]

    :rtype: Dict[str, object]
    """
    return 'do some magic!'


def move(data_source_id, request_body):  # noqa: E501
    """Move document

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param request_body: Object containing all info for a document
    :type request_body: Dict[str, ]

    :rtype: Dict[str, object]
    """
    return 'do some magic!'


def remove(data_source_id, inline_object2):  # noqa: E501
    """Remove document

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param inline_object2: 
    :type inline_object2: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        inline_object2 = InlineObject2.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def remove_by_path(data_source_id, inline_object3):  # noqa: E501
    """Remove document by path

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param inline_object3: 
    :type inline_object3: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        inline_object3 = InlineObject3.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def rename(data_source_id, inline_object4):  # noqa: E501
    """Rename document

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param inline_object4: 
    :type inline_object4: dict | bytes

    :rtype: Dict[str, object]
    """
    if connexion.request.is_json:
        inline_object4 = InlineObject4.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
