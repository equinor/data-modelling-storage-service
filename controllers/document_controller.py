from typing import Optional

from fastapi import APIRouter
from pydantic import conint
from starlette.responses import JSONResponse

from api.core.use_case.get_document_by_path_use_case import GetDocumentByPathRequest, GetDocumentByPathUseCase
from api.core.use_case.get_document_use_case import GetDocumentRequest, GetDocumentUseCase
from api.core.use_case.update_document_use_case import UpdateDocumentRequest, UpdateDocumentUseCase
from controllers.status_codes import STATUS_CODES

router = APIRouter()


@router.get("/documents/{data_source_id}/{document_id}")
def get_by_id(
    data_source_id: str,
    document_id: str,
    ui_recipe: Optional[str] = None,
    attribute: Optional[str] = None,
    depth: conint(gt=0, lt=1000) = 999,
):
    use_case = GetDocumentUseCase()
    response = use_case.execute(
        GetDocumentRequest(
            data_source_id=data_source_id,
            document_id=document_id,
            ui_recipe=ui_recipe,
            attribute=attribute,
            depth=depth,
        )
    )

    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.get("/documents-by-path/{data_source_id}")
def get_by_path(
    data_source_id: str, ui_recipe: Optional[str] = None, attribute: Optional[str] = None, path: Optional[str] = None
):
    """
    Get a document by it's path in the form "{dataSource}/{rootPackage}/{subPackage(s)?/{name}
    """
    use_case = GetDocumentByPathUseCase()
    response = use_case.execute(
        GetDocumentByPathRequest(data_source_id=data_source_id, path=path, ui_recipe=ui_recipe, attribute=attribute)
    )
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.put("/documents/{data_source_id}/{document_id}")
def update(data_source_id: str, document_id: str, data: dict, attribute: Optional[str] = None):
    update_use_case = UpdateDocumentUseCase()
    response = update_use_case.execute(
        UpdateDocumentRequest(data_source_id=data_source_id, data=data, document_id=document_id, attribute=attribute)
    )
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
