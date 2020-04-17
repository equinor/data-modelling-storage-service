from api.core.shared import response_object, use_case
from api.core.shared import request_object as req


class GetDataSourceUseCaseRequestObject(req.ValidRequestObject):
    def __init__(self, data_source_id):
        self.data_source_id = data_source_id

    @classmethod
    def from_dict(cls, adict):
        invalid_req = req.InvalidRequestObject()

        if "data_source_id" not in adict:
            invalid_req.add_error("data_source_id", "is missing")

        if invalid_req.has_errors():
            return invalid_req

        return cls(data_source_id=adict.get("data_source_id"),)


class GetDataSourceUseCase(use_case.UseCase):
    def __init__(self, data_source_repository):
        self.data_source_repository = data_source_repository

    def process_request(self, request_object: GetDataSourceUseCaseRequestObject):
        data_source_id: str = request_object.data_source_id

        data_sources = self.data_source_repository.get(data_source_id)
        return response_object.ResponseSuccess(data_sources)
