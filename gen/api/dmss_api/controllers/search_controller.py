import connexion
import six

from dmss_api.models.inline_object5 import InlineObject5  # noqa: E501
from dmss_api import util


def search_entities(data_source_id, inline_object5):  # noqa: E501
    """Search for entities

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param inline_object5: 
    :type inline_object5: dict | bytes

    :rtype: Dict[str, object]
    """
    if connexion.request.is_json:
        inline_object5 = InlineObject5.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
