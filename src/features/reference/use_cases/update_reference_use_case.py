from authentication.models import User
from common.address import Address
from restful.request_types.shared import ReferenceEntity
from services.document_service import DocumentService


def update_reference_use_case(user: User, address: str, reference: ReferenceEntity):
    document_service = DocumentService(user=user)
    return document_service.update_reference(Address.from_absolute(address), reference)
