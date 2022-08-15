from typing import Optional

from authentication.models import User
from restful.request_types.shared import DataSource
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source
from common.utils.get_document_by_path import get_document_by_ref


def get_document_by_path_use_case(
    user: User,
    data_source_id: str,
    path: Optional[str] = None,
    attribute: Optional[str] = None,
    repository_provider=get_data_source,
):
    document_service = DocumentService(repository_provider=repository_provider, user=user)

    data_source_id: str = data_source_id
    root_doc = get_document_by_ref(f"{data_source_id}/{path}", user)
    document = document_service.get_node_by_uid(data_source_id=data_source_id, document_uid=root_doc["_id"])

    if attribute:
        document = document.get_by_path(attribute.split("."))

    return document.to_dict()
