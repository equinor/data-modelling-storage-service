from typing import List, Optional, Union

from pydantic import conint
from starlette.responses import JSONResponse

from authentication.models import User
from services.document_service import DocumentService
from restful.request_types.shared import DataSource

from restful.use_case import UseCase
from storage.internal.data_source_repository import get_data_source


class GetDocumentRequest(DataSource):
    document_id: str
    ui_recipe: Optional[str] = None
    attribute: Optional[str] = None
    depth: conint(gt=-1, lt=1000) = 999


def get_nested_dict_attribute(entity: Union[dict, list], path_list: List[str]) -> Union[dict, list]:
    try:
        if isinstance(entity, list):
            path_list[0] = int(path_list[0])
        if len(path_list) == 1:
            return entity[path_list[0]]
        return get_nested_dict_attribute(entity[path_list[0]], path_list[1:])
    except (KeyError, IndexError):
        raise KeyError(f"Attribute/Item '{path_list[0]}' does not exists in '{entity}'")


class GetDocumentUseCase(UseCase):
    def __init__(self, user: User, repository_provider=get_data_source):
        self.repository_provider = repository_provider
        self.document_service = DocumentService(repository_provider=self.repository_provider, user=user)

    def process_request(self, req: GetDocumentRequest):
        attribute: str = req.attribute
        attribute_depth = len(attribute.split(".")) if attribute else 0
        document = self.document_service.get_document_by_uid(
            data_source_id=req.data_source_id,
            document_uid=req.document_id,
            depth=req.depth + attribute_depth,
        )

        # TODO: Pass attribute to DocumentService.get_document_by_uid and only cound depth from the attribute leaf node
        if attribute:
            document = get_nested_dict_attribute(document, attribute.split("."))

        return JSONResponse(document)
