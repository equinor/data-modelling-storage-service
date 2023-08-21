from authentication.models import AccessControlList, User
from services.document_service import DocumentService


def get_acl_use_case(user: User, document_id: str, data_source_id: str):
    document_service = DocumentService(user=user)
    acl: AccessControlList = document_service.get_access_control_list(
        data_source_id=data_source_id, document_id=document_id
    )
    return acl
