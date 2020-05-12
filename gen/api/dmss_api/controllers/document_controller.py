import connexion
import six

from dmss_api import util


def get_by_id(data_source_id, document_id):  # noqa: E501
    """Get document by ID

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param document_id: The document ID
    :type document_id: str

    :rtype: Dict[str, object]
    """
    return 'do some magic!'


def get_by_path(data_source_id, path):  # noqa: E501
    """Get document by path

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param path: The document path
    :type path: str

    :rtype: Dict[str, object]
    """
    return 'do some magic!'


def update(data_source_id, document_id, request_body, attribute=None):  # noqa: E501
    """Update document

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param document_id: The document ID
    :type document_id: str
    :param request_body: Object containing all info for a document
    :type request_body: Dict[str, ]
    :param attribute: Path to contained document
    :type attribute: str

    :rtype: Dict[str, object]
    """
    return 'do some magic!'
