from typing import List, Optional, Union

from fastapi import File, UploadFile

from authentication.models import User
from common.reference import Reference
from enums import SIMOS
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def update_document_use_case(
    user: User,
    reference: str,
    data: Union[dict, list],
    files: Optional[List[UploadFile]] = File(None),
    update_uncontained: Optional[bool] = True,
    repository_provider=get_data_source,
):
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    document = document_service.update_document(
        Reference.fromabsolute(reference),
        data,
        files={f.filename: f.file for f in files} if files else None,
        update_uncontained=update_uncontained,
    )
    # Do not invalidate the blueprint cache if it was not a blueprint that was changed
    if "type" in document["data"] and document["data"]["type"] == SIMOS.BLUEPRINT.value:
        document_service.invalidate_cache()
    return document
