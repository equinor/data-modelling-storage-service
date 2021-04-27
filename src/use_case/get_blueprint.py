from restful import response_object as res
from restful import use_case as uc
from restful.request_types.shared import EntityType
from services.document_service import DocumentService


class GetBlueprintUseCase(uc.UseCase):
    def process_request(self, type: EntityType):
        document_service = DocumentService()
        blueprint = document_service.get_blueprint(type)
        return res.ResponseSuccess(blueprint.to_dict())
