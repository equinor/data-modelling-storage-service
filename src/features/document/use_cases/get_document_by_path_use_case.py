from authentication.models import User
from common.utils.get_document_by_path import get_document_by_absolute_path
from common.utils.string_helpers import split_dmss_ref
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source


def get_document_by_path_use_case(
    user: User,
    absolute_path: str,
    repository_provider=get_data_source,
):
    """Fetch an entity based on 'absolute path'.
    The format would look like; PROTOCOL://ROOT_PACKAGE/ENTITY.Attribute"""
    document_service = DocumentService(repository_provider=repository_provider, user=user)

    root_doc = get_document_by_absolute_path(absolute_path, user)
    protocol, address = absolute_path.split("://", 1)

    match protocol:
        case "dmss":  # The document should be fetched from a DataSource in this DMSS instance
            data_source_id, path, attribute = split_dmss_ref(address)
            document = document_service.get_node_by_uid(data_source_id=data_source_id, document_uid=root_doc["_id"])
        case "http":  # The document should be fetched by an HTTP call
            raise NotImplementedError
        case _:
            raise NotImplementedError

    if attribute:
        document = document.get_by_path(attribute.split("."))

    return document.to_dict()
