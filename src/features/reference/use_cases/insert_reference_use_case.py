from authentication.models import User
from restful.request_types.shared import Reference
from services.document_service import DocumentService


# todo data_source_id requirements
def insert_reference_use_case(user: User, data_source_id: str, document_id: str, reference: Reference, attribute: str):
    document_service = DocumentService(user=user)
    document = document_service.insert_reference(
        data_source_id=data_source_id,
        document_id=document_id,
        reference=reference,
        attribute_path=attribute,
    )
    return document
