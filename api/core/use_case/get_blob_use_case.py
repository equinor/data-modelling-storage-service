from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.storage.internal.data_source_repository import get_data_source
from api.request_types.shared import DataSource


class GetBlobRequest(DataSource):
    blob_id: str


class GetBlobUseCase(uc.UseCase):
    def process_request(self, req: GetBlobRequest):
        data_source = get_data_source(req.data_source_id)
        blob = data_source.get_blob(req.blob_id)
        return res.ResponseSuccess(blob)
