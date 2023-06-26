from authentication.models import User
from common.address import Address
from services.document_service import DocumentService


def delete_reference_use_case(user: User, address: str):
    document_service = DocumentService(user=user)
    return document_service.remove_reference(Address.from_absolute(address))
