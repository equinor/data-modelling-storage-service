from restful.use_case import UseCase
from restful import response_object as res
from storage.internal.data_source_repository import get_data_source
from services.document_service import DocumentService

class FindPackagesRequest():
    def __init__(self, data_source_id: str, document_id: str):
        self.data_source_id = data_source_id
        self.document_id = document_id

class FindPackagesUseCase(UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider

    def process_request(self, req: FindPackagesRequest):
        document_service = DocumentService(repository_provider=self.repository_provider)
        list_of_packages = document_service.find_packages(data_source_id=req.data_source_id, document_id=req.document_id)
        return res.ResponseSuccess(list_of_packages)
