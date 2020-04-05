from typing import Dict

from api.core.shared import request_object as req
from api.core.shared import response_object as res
from api.core.shared import use_case as uc
from api.core.use_case.utils.get_related_blueprints import get_related_blueprints


class GetBlueprintsRequestObject(req.ValidRequestObject):
    def __init__(self, blueprint):
        self.blueprint = blueprint


class GetBlueprintsUseCase(uc.UseCase):
    def process_request(self, request_object: GetBlueprintsRequestObject):
        blueprint: str = request_object.blueprint

        related_blueprints: Dict = get_related_blueprints(blueprint)

        return res.ResponseSuccess(related_blueprints)
