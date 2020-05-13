from api.core.storage.internal.data_source_repository import get_data_source
from api.core.service.document_service import DocumentService
from api.core.shared import request_object as req
from api.core.shared import response_object as res
from api.core.shared import use_case as uc


class AddDocumentToPathRequestObject(req.ValidRequestObject):
    def __init__(
        self, data_source_id=None, directory=None, document=None,
    ):
        self.data_source_id = data_source_id
        self.directory = directory
        self.document = document

    @classmethod
    def from_dict(cls, adict):
        invalid_req = req.InvalidRequestObject()

        if "document" not in adict:
            invalid_req.add_error("document", "is missing")

        if "directory" not in adict:
            invalid_req.add_error("directory", "is missing")

        if "data_source_id" not in adict:
            invalid_req.add_error("data_source_id", "is missing")

        if invalid_req.has_errors():
            return invalid_req

        return cls(
            data_source_id=adict.get("data_source_id"),
            document=adict.get("document"),
            directory=adict.get("directory"),
        )


class AddDocumentToPathUseCase(uc.UseCase):
    def __init__(self, repository_provider=get_data_source):
        self.repository_provider = repository_provider

    def process_request(self, request_object: AddDocumentToPathRequestObject):
        data_source_id = request_object.data_source_id
        directory: str = request_object.directory
        document: str = request_object.document

        document_service = DocumentService(repository_provider=self.repository_provider)
        document = document_service.add(data_source_id=data_source_id, directory=directory, document=document)
        return res.ResponseSuccess(document)
