from authentication.models import User
from common.utils.string_helpers import split_dmss_ref
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def remove_use_case(user: User, id_reference: str, repository_provider=get_data_source):
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    data_source_id, document_id, attribute = split_dmss_ref(id_reference)
    document_service.remove_document(data_source_id, document_id, attribute)
    document_service.invalidate_cache()
    return "OK"
