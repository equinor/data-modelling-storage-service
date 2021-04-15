from restful import response_object as res
from restful import use_case as uc
from restful.request_types.shared import DataSource
from storage.internal.data_source_repository import get_data_source


class GetBlobRequest(DataSource):
    blob_id: str


class GetBlobUseCase(uc.UseCase):
    def process_request(self, req: GetBlobRequest):
        data_source = get_data_source(req.data_source_id)
        blob = data_source.get_blob(req.blob_id)
        return res.ResponseSuccess(blob)
