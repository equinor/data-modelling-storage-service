from domain_classes.user import User
from restful import response_object as res
from restful import use_case as uc
from services.document_service import DocumentService


class ExportUseCase(uc.UseCase):
    def __init__(self, user: User):
        self.user = user

    def process_request(self, request_object: str):
        memory_file = DocumentService(user=self.user).create_zip_export(request_object)
        return res.ResponseSuccess(memory_file)
