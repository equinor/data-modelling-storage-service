from authentication.models import User
from common.reference import Reference
from services.document_service import DocumentService


def delete_reference_use_case(user: User, data_source_id: str, document_dotted_id: str):
    document_service = DocumentService(user=user)
    return document_service.remove_reference(Reference(document_dotted_id, data_source_id))
