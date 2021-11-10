from domain_classes.user import User
from services.document_service import DocumentService
from restful import response_object as res
from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source


class AddFileUseCase(UseCase):
    def __init__(self, user: User, repository_provider=get_data_source):
        self.user = user
        self.repository_provider = repository_provider

    def process_request(self, req: dict):
        document_service = DocumentService(repository_provider=self.repository_provider, user=self.user)
        document = document_service.add_document(
            absolute_ref=req["absolute_ref"], data=req["data"], update_uncontained=req["update_uncontained"]
        )
        document_service.invalidate_cache()
        return res.ResponseSuccess(document)
