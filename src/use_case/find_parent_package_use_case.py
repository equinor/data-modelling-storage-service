from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source
from services.document_service import DocumentService

class FindParentPackageRequest():
    def __init__(self, data_source_id: str, document_id: str):
        self.data_source_id = data_source_id
        self.document_id = document_id

class FindParentPackageUseCase(UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider

    def process_request(self, req: FindParentPackageRequest):
        document_service = DocumentService(repository_provider=self.repository_provider)
        package_id, is_root = document_service.find_parent_package(data_source_id=req.data_source_id, document_id=req.document_id)
        return package_id, is_root
