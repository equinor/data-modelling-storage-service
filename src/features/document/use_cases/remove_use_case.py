from authentication.models import User
from common.address import Address
from services.document_service.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def remove_use_case(user: User, address: str, repository_provider=get_data_source) -> str:
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    document_service.remove(Address.from_absolute(address))
    document_service.invalidate_cache()
    return "OK"
