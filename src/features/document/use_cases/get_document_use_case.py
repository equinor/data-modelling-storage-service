from typing import List, Union

from pydantic import conint

from authentication.models import User
from common.utils.string_helpers import split_absolute_ref
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def get_nested_dict_attribute(entity: Union[dict, list], path_list: List[str]) -> Union[dict, list]:
    try:
        if isinstance(entity, list):
            path_list[0] = int(path_list[0])
        if len(path_list) == 1:
            return entity[path_list[0]]
        return get_nested_dict_attribute(entity[path_list[0]], path_list[1:])
    except (KeyError, IndexError):
        raise KeyError(f"Attribute/Item '{path_list[0]}' does not exists in '{entity}'")


def get_document_use_case(
    user: User,
    absolute_id: str,
    depth: conint(gt=-1, lt=1000) = 999,
    repository_provider=get_data_source,
):
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    data_source_id, document_id, attribute = split_absolute_ref(absolute_id)
    attribute: str = attribute
    attribute_depth = len(attribute.split(".")) if attribute else 0
    document = document_service.get_document_by_uid(
        data_source_id=data_source_id,
        document_uid=document_id,
        depth=depth + attribute_depth,
    )

    # TODO: Pass attribute to DocumentService.get_document_by_uid and only count depth from the attribute leaf node
    if attribute:
        document = get_nested_dict_attribute(document, attribute.split("."))

    return document
