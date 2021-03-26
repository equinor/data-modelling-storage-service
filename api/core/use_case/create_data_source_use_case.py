from api.core.shared import response_object, use_case
from api.request_types.create_data_source import DataSourceRequest
from api.request_types.shared import DataSource


class CreateDataSourceRequest(DataSource):
    new_data_source: DataSourceRequest


class CreateDataSourceUseCase(use_case.UseCase):
    def __init__(self, data_source_repository):
        self.data_source_repository = data_source_repository

    def process_request(self, req: CreateDataSourceRequest):
        response = self.data_source_repository.create(req.data_source_id, req.new_data_source)
        return response_object.ResponseSuccess(response)
