from authentication.models import User
from storage.internal.data_source_repository import get_data_source


def get_meta_use_case(user: User, data_source_id: str, document_id: str):
    data_source = get_data_source(data_source_id, user)
    if document_id.startswith("$"):
        document_id = document_id[1:]
    lookup = data_source.get_lookup(document_id)
    return lookup.meta
