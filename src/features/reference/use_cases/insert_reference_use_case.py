from authentication.models import User
from common.reference import Reference
from restful.request_types.shared import ReferenceEntity
from services.document_service import DocumentService


def insert_reference_use_case(user: User, data_source_id: str, document_dotted_id: str, reference: ReferenceEntity):
    document_service = DocumentService(user=user)
    return document_service.insert_reference(Reference(document_dotted_id, data_source_id), reference)
