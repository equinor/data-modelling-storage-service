from restful import response_object as res
from restful import use_case as uc
from services.document_service import DocumentService


class ExportUseCase(uc.UseCase):
    def process_request(self, request_object: str):
        memory_file = DocumentService().create_zip_export(request_object)
        return res.ResponseSuccess(memory_file)
