from api.core.repository.repository_factory import get_repository
from api.core.service.document_service import DocumentService
from api.core.shared import request_object as req
from api.core.shared import response_object as res
from api.core.shared import use_case as uc


class RemoveByPathRequestObject(req.ValidRequestObject):
    def __init__(self, data_source_id=None, directory=None):
        self.data_source_id = data_source_id
        self.directory = directory

    @classmethod
    def from_dict(cls, adict):
        invalid_req = req.InvalidRequestObject()

        if "data_source_id" not in adict:
            invalid_req.add_error("data_source_id", "is missing")

        if "directory" not in adict:
            invalid_req.add_error("directory", "is missing")

        if invalid_req.has_errors():
            return invalid_req

        return cls(data_source_id=adict.get("data_source_id"), directory=adict.get("directory"))


class RemoveByPathUseCase(uc.UseCase):
    def __init__(self, repository_provider=get_repository):
        self.repository_provider = repository_provider

    def process_request(self, request_object):
        data_source_id: str = request_object.data_source_id
        directory: str = request_object.directory

        document_service = DocumentService(repository_provider=self.repository_provider)
        document_service.remove_by_path(data_source_id, directory)
        document_service.invalidate_cache()
        return res.ResponseSuccess(True)
