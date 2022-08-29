from authentication.models import User
from storage.internal.data_source_repository import get_data_source


def get_blob_use_case(user: User, data_source_id: str, blob_id: str):
    data_source = get_data_source(data_source_id, user)
    blob = data_source.get_blob(blob_id)
    return blob
