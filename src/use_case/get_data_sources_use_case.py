from starlette.responses import JSONResponse

from restful.use_case import UseCase


class GetDataSourcesUseCase(UseCase):
    def __init__(self, data_source_repository):
        self.data_source_repository = data_source_repository

    def process_request(self, request_object=None):
        return JSONResponse(self.data_source_repository.list())
