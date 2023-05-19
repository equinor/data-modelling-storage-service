from fastapi import UploadFile

from authentication.models import User
from enums import SIMOS
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def add_use_case(
    user: User,
    reference: str,
    data: dict,
    files: list[UploadFile] | None = None,
    update_uncontained: bool = True,
    repository_provider=get_data_source,
):
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    document = document_service.add(
        reference=reference,
        entity=data,
        update_uncontained=update_uncontained,
        files={f.filename: f.file for f in files} if files else None,
    )
    # Do not invalidate the blueprint cache if it was not a blueprint that was changed
    if data["type"] == SIMOS.BLUEPRINT.value:
        document_service.invalidate_cache()

    return document
