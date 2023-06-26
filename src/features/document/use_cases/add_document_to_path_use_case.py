from typing import List, Optional

from fastapi import UploadFile

from authentication.models import User
from common.address import Address
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def add_document_use_case(
    user: User,
    document: dict,
    address: str,
    files: Optional[List[UploadFile]] = None,
    update_uncontained: Optional[bool] = False,
    repository_provider=get_data_source,
):
    document_service = DocumentService(repository_provider=repository_provider, user=user)

    document = document_service.add(
        address=Address.from_absolute(address),
        document=document,
        files={f.filename: f.file for f in files} if files else None,
        update_uncontained=update_uncontained,
    )

    return document
