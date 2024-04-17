from fastapi import UploadFile

from authentication.models import User
from storage.internal.get_data_source_cached import get_data_source_cached


def upload_blob_use_case(user: User, data_source_id: str, blob_id: str, file: UploadFile):
    data_source = get_data_source_cached(data_source_id, user)
    data_source.update_blob(blob_id, file.filename, file.content_type, file.file)
    return "OK"
