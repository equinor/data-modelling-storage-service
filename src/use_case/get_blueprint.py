from authentication.models import User
from restful import response_object as res
from restful import use_case as uc
from restful.request_types.shared import EntityType
from services.document_service import DocumentService


class GetBlueprintUseCase(uc.UseCase):
    def __init__(self, user: User):
        self.user = user

    def process_request(self, type: EntityType):
        document_service = DocumentService(user=self.user)
        blueprint = document_service.get_blueprint(type)
        return res.ResponseSuccess(blueprint.to_dict())
