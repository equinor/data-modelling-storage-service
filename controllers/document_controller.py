from typing import Optional

from fastapi import APIRouter
from starlette.responses import JSONResponse

from api.core.use_case.get_document_by_path_use_case import GetDocumentByPathRequestObject, GetDocumentByPathUseCase
from api.core.use_case.get_document_use_case import GetDocumentRequestObject, GetDocumentUseCase
from api.core.use_case.update_document_use_case import UpdateDocumentRequestObject, UpdateDocumentUseCase
from controllers.status_codes import STATUS_CODES

router = APIRouter()


@router.get("/documents/{data_source_id}/{document_id}")
def get_by_id(data_source_id: str, document_id: str, ui_recipe: Optional[str] = None, attribute: Optional[str] = None,
              depth: int = 999):
    use_case = GetDocumentUseCase()
    request_object = GetDocumentRequestObject.from_dict(
        {
            "data_source_id": data_source_id,
            "document_id": document_id,
            "ui_recipe": ui_recipe,
            "attribute": attribute,
            "depth": depth,
        }
    )
    response = use_case.execute(request_object)

    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.get("/documents-by-path/{data_source_id}")
def get_by_path(data_source_id: str, ui_recipe: Optional[str] = None, attribute: Optional[str] = None,
                path: Optional[str] = None):
    use_case = GetDocumentByPathUseCase()
    request_object = GetDocumentByPathRequestObject.from_dict(
        {"data_source_id": data_source_id, "path": path, "ui_recipe": ui_recipe, "attribute": attribute}
    )
    response = use_case.execute(request_object)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.put("/documents/{data_source_id}/{document_id}")
def update(data_source_id: str, document_id: str, attribute: Optional[str] = None, data: Optional[dict] = None):
    request_object = UpdateDocumentRequestObject.from_dict(
        {"data_source_id": data_source_id, "data": data, "document_id": document_id, "attribute": attribute}
    )
    update_use_case = UpdateDocumentUseCase()
    response = update_use_case.execute(request_object)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
