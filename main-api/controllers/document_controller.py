import connexion
import six
from dmss_api.models import DocumentResponse

def get_document(data_source_id, document_id):  # noqa: E501
    """Get document

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str

    :rtype: DocumentRepsonse
    """
    return DocumentResponse(document={})
