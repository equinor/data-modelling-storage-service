from authentication.models import ACL, User


from services.document_service import DocumentService


def get_acl_use_case(user: User, document_id: str, data_source_id: str):
    document_service = DocumentService(user=user)
    acl: ACL = document_service.get_acl(data_source_id=data_source_id, document_id=document_id)
    return acl
