import connexion
import six

from dmss_api.models.inline_response200 import InlineResponse200  # noqa: E501
from dmss_api import util


def get_all():  # noqa: E501
    """Get all data sources

     # noqa: E501


    :rtype: List[object]
    """
    return 'do some magic!'


def get_data_source(data_source_id):  # noqa: E501
    """Get data source

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str

    :rtype: Dict[str, object]
    """
    return 'do some magic!'


def save(data_source_id, request_body):  # noqa: E501
    """Add data source

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param request_body: Object containing all info for a document
    :type request_body: Dict[str, ]

    :rtype: InlineResponse200
    """
    return 'do some magic!'
