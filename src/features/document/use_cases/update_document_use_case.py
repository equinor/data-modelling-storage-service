from typing import List, Optional, Union

from fastapi import File, UploadFile

from authentication.models import User
from common.utils.string_helpers import split_dmss_ref
from enums import SIMOS
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def update_document_use_case(
    user: User,
    id_reference: str,
    data: Union[dict, list],
    files: Optional[List[UploadFile]] = File(None),
    repository_provider=get_data_source,
):
    data_source_id, document_id, attribute = split_dmss_ref(id_reference)
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    document = document_service.update_document(
        data_source_id=data_source_id,
        document_id=document_id,
        attribute=attribute,
        data=data,
        files={f.filename: f.file for f in files} if files else None,
    )
    # Do not invalidate the blueprint cache if it was not a blueprint that was changed
    if "type" in document["data"] and document["data"]["type"] == SIMOS.BLUEPRINT.value:
        document_service.invalidate_cache()
    return document
