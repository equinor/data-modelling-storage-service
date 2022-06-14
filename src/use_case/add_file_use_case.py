from enums import SIMOS
from starlette.responses import JSONResponse

from authentication.models import User
from services.document_service import DocumentService
from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source
from utils.string_helpers import split_absolute_ref


class AddFileUseCase(UseCase):
    def __init__(self, user: User, repository_provider=get_data_source):
        self.user = user
        self.repository_provider = repository_provider

    def process_request(self, req: dict):
        document_service = DocumentService(repository_provider=self.repository_provider, user=self.user)
        document = document_service.add_document(
            absolute_ref=req["absolute_ref"], data=req["data"], update_uncontained=req["update_uncontained"]
        )
        # Do not invalidate the blueprint cache if it was not a blueprint that was changed
        if req["data"]["type"] == SIMOS.BLUEPRINT.value:
            document_service.invalidate_cache()

        data_source, _, _ = split_absolute_ref(req["absolute_ref"])
        return JSONResponse(document)
