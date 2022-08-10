from authentication.models import User
from services.document_service import DocumentService


def export_user_case(user: User, document_reference: str):
    memory_file = DocumentService(user=user).create_zip_export(document_reference)
    return memory_file
