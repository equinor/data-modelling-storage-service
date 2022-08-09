from authentication.models import ACL, User
from services.document_service import DocumentService


def set_acl_use_case(user: User, data_source_id: str, document_id: str, acl: ACL, recursively: bool):
    document_service = DocumentService(user=user)
    document_service.set_acl(data_source_id=data_source_id, document_id=document_id, acl=acl, recursively=recursively)
    return "OK"
