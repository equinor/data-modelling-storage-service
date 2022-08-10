from typing import List, Optional, Union

from enums import SIMOS
from fastapi import File, UploadFile

from authentication.models import User


from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source

# todo requirements on data_source_id string
def update_document_use_case(
    user: User,
    document_id: str,
    data_source_id: str,
    data: Union[dict, list],
    attribute: Optional[str] = None,
    files: Optional[List[UploadFile]] = File(None),
    update_uncontained: Optional[bool] = True,
    repository_provider=get_data_source,
):
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    if attribute and "." in document_id:
        raise ValueError(
            "Attribute may only be specified in ether dotted path on "
            + "documentId or the 'attribute' query parameter"
        )
    attribute = attribute if attribute else ""
    dotted_id = document_id + attribute
    document = document_service.update_document(
        data_source_id=data_source_id,
        dotted_id=dotted_id,
        data=data,
        files={f.filename: f.file for f in files} if files else None,
        update_uncontained=update_uncontained,
    )
    # Do not invalidate the blueprint cache if it was not a blueprint that was changed
    if document["data"]["type"] == SIMOS.BLUEPRINT.value:
        document_service.invalidate_cache()
    return document
