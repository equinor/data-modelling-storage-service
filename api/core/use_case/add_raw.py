from uuid import uuid4

from api.classes.dto import DTO
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.storage.internal.data_source_repository import get_data_source
from api.core.utility import BlueprintProvider
from api.request_types.shared import DataSource, NamedEntity


class AddRawRequest(DataSource):
    document: NamedEntity


class AddRawUseCase(uc.UseCase):
    def __init__(self, blueprint_provider=BlueprintProvider()):
        self.blueprint_provider = blueprint_provider

    def process_request(self, req: AddRawRequest):
        uid: str = req.document.uid
        new_node_id = str(uuid4()) if not uid else uid
        document: DTO = DTO(uid=new_node_id, data=req.document.dict())
        document_repository = get_data_source(req.data_source_id)
        document_repository.add(document)
        return res.ResponseSuccess(new_node_id)
