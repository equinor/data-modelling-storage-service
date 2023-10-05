from common.address import Address
from common.exceptions import NotFoundException
from services.document_service.document_service import DocumentService


def check_existence_use_case(address: Address, document_service: DocumentService) -> bool:
    try:
        document_service.get_document(address)
        return True
    except NotFoundException:
        return False
