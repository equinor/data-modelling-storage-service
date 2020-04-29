import connexion
import six

from dmss_api.models.inline_object3 import InlineObject3  # noqa: E501
from dmss_api import util


def search_entities(data_source_id, inline_object3):  # noqa: E501
    """Search for entities

     # noqa: E501

    :param data_source_id: The data source ID
    :type data_source_id: str
    :param inline_object3: 
    :type inline_object3: dict | bytes

    :rtype: Dict[str, object]
    """
    if connexion.request.is_json:
        inline_object3 = InlineObject3.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
