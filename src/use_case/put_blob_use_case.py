from fastapi import UploadFile
from starlette.responses import PlainTextResponse

from authentication.models import User
from restful import use_case as uc
from restful.request_types.shared import DataSource
from storage.internal.data_source_repository import get_data_source


class PutBlobRequest(DataSource):
    blob_id: str
    file: UploadFile


class PutBlobUseCase(uc.UseCase):
    def __init__(self, user: User):
        self.user = user

    def process_request(self, req: PutBlobRequest):
        data_source = get_data_source(req.data_source_id, self.user)
        data_source.update_blob(req.blob_id, req.file.file)
        return PlainTextResponse("Ok")
