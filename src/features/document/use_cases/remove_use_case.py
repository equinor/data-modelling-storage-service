from authentication.models import User
from common.address import Address
from services.document_service.document_service import DocumentService


def remove_use_case(user: User, address: str) -> str:
    document_service = DocumentService(user=user)
    document_service.remove(Address.from_absolute(address))
    document_service.invalidate_cache()
    return "OK"
