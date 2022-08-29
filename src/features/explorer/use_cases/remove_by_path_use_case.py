from typing import Optional
from authentication.models import User
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def remove_by_path_use_case(
    user: User, directory: str, data_source_id: Optional[str] = None, repository_provider=get_data_source
):
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    document_service.remove_by_path(data_source_id, directory)
    document_service.invalidate_cache()
    return "OK"
