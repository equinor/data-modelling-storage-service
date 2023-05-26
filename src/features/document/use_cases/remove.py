from authentication.models import User
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def remove_use_case(user: User, reference: str, repository_provider=get_data_source):
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    document_service.remove(reference)
    document_service.invalidate_cache()
    return "OK"
