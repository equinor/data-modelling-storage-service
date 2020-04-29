import connexion
import six

from dmss_api import util


def find_by_name(data_source_id, name):  # noqa: E501
    """Query packages

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param name: The name of the package to find
    :type name: str

    :rtype: object
    """
    return 'do some magic!'


def get(data_source_id):  # noqa: E501
    """Get packages

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str

    :rtype: List[object]
    """
    return 'do some magic!'
