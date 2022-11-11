from typing import List, Optional

from fastapi import UploadFile

from authentication.models import User
from common.utils.string_helpers import split_absolute_ref
from restful.request_types.shared import Entity
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def add_document_to_path_use_case(
    user: User,
    document: dict,
    absolute_ref: str,
    files: Optional[List[UploadFile]] = None,
    update_uncontained: Optional[bool] = False,
    repository_provider=get_data_source,
):
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    request_document: Entity = Entity(**document)
    data_source_id, path, attribute = split_absolute_ref(absolute_ref)
    document = document_service.add(
        data_source_id=data_source_id,
        path=path,
        document=request_document,
        files={f.filename: f.file for f in files} if files else None,
        update_uncontained=update_uncontained,
    )

    return document
