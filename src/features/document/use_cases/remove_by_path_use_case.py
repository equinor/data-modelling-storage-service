from authentication.models import User
from common.utils.string_helpers import split_dmss_ref
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def remove_by_path_use_case(user: User, absolute_path: str, repository_provider=get_data_source):
    document_service = DocumentService(repository_provider=repository_provider, user=user)
    data_source_id, directory, attribute = split_dmss_ref(absolute_path)
    document_service.remove_by_path(data_source_id, directory)
    document_service.invalidate_cache()
    return "OK"
