from starlette.responses import FileResponse

from authentication.models import User
from restful import use_case as uc
from services.document_service import DocumentService


class ExportUseCase(uc.UseCase):
    def __init__(self, user: User):
        self.user = user

    def process_request(self, request_object: str):
        memory_file = DocumentService(user=self.user).create_zip_export(request_object)
        response = FileResponse(memory_file, media_type="application/zip")
        response.headers["Content-Disposition"] = "attachment; filename=dmt-export.zip"
        return response
