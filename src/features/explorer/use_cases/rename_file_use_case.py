from typing import Optional

from authentication.models import User
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


# todo entity name has requirements: constr(min_length=1, max_length=128, regex=name_regex, strip_whitespace=True)
def rename_use_case(
    user: User,
    name: str,
    document_id: str,
    data_source_id: Optional[str] = None,
    parent_id: Optional[str] = None,
    repository_provider=get_data_source,
):
    # This use case is not working correctly.
    raise NotImplementedError
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    document = document_service.rename_document(
        data_source_id=data_source_id,
        document_id=document_id,
        parent_uid=parent_id,
        name=name,
    )
    document_service.invalidate_cache()
    return document
