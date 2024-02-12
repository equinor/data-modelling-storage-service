from datetime import datetime
from uuid import uuid4

from fastapi import UploadFile

from authentication.models import User
from enums import REFERENCE_TYPES, SIMOS
from storage.internal.data_source_repository import get_data_source


async def add_file_use_case(data_source_id: str, file_id: str, file: UploadFile, user: User):
    blob_id = str(uuid4())
    data_source = get_data_source(data_source_id, user)
    data_source.update_blob(blob_id, file.filename, file.content_type, file.file)
    await file.seek(0)
    content = await file.read()
    file_size = len(content)
    # The reference to the binary data needs to be of type pointer
    # to avoid it to be resolved in get_resolved_document_by_id.
    # TODO: Create a File and Reference class and use that

    filename_parts = file.filename.split(".")
    document = {
        "_id": file_id,
        "type": SIMOS.FILE.value,
        "name": filename_parts[0],
        "author": user.full_name if user.full_name else "",
        "date": f"{datetime.now()}",
        "size": file_size, 
        "filetype": filename_parts[1] if len(filename_parts) > 1 else "",
        "contentType": file.content_type,
        "content": {
            "type": SIMOS.REFERENCE.value,
            "address": f"${blob_id}",
            "referenceType": REFERENCE_TYPES.STORAGE.value,
        },
    }
    data_source.update(document)
    return document
