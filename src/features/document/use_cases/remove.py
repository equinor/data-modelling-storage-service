from authentication.models import User
from common.reference import Reference
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def remove_use_case(user: User, reference: str, repository_provider=get_data_source) -> str:
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    document_service.remove(Reference.fromabsolute(reference))
    document_service.invalidate_cache()
    return "OK"
