from authentication.models import User
from services.document_service import DocumentService


# todo data_source_id has requirements
def delete_reference_use_case(user: User, data_source_id: str, document_id: str, attribute: str):
    document_service = DocumentService(user=user)
    document = document_service.remove_reference(
        data_source_id=data_source_id,
        document_id=document_id,
        attribute_path=attribute,
    )
    return document
