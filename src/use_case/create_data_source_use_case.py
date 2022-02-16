from starlette.responses import JSONResponse

from restful import use_case
from restful.request_types.create_data_source import DataSourceRequest
from restful.request_types.shared import DataSource


class CreateDataSourceRequest(DataSource):
    new_data_source: DataSourceRequest


class CreateDataSourceUseCase(use_case.UseCase):
    def __init__(self, data_source_repository):
        self.data_source_repository = data_source_repository

    def process_request(self, req: CreateDataSourceRequest):
        response = self.data_source_repository.create(req.data_source_id, req.new_data_source)
        return JSONResponse(response)
