from authentication.models import User
from storage.internal.get_data_source_cached import get_data_source_cached


def get_blob_use_case(user: User, data_source_id: str, blob_id: str):
    data_source = get_data_source_cached(data_source_id, user)
    if blob_id.startswith("$"):
        blob_id = blob_id[1:]
    blob = data_source.get_blob(blob_id)
    return blob
