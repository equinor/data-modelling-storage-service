import connexion
import six

from dmss_api import util


def search_entities(data_source_id, request_body):  # noqa: E501
    """Search for entities

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param request_body: A JSON object containing search parameters
    :type request_body: Dict[str, ]

    :rtype: Dict[str, object]
    """
    return 'do some magic!'
