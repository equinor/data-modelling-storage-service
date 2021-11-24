from typing import List, Optional

from fastapi import APIRouter, File, Form, UploadFile, Depends
from pydantic import conint, Json
from starlette.responses import JSONResponse

from authentication.authentication import get_current_user
from domain_classes.user import User
from restful.status_codes import STATUS_CODES
from use_case.get_document_by_path_use_case import GetDocumentByPathRequest, GetDocumentByPathUseCase
from use_case.get_document_use_case import GetDocumentRequest, GetDocumentUseCase
from use_case.get_document_use_case import GetDocumentResponse
from use_case.update_document_use_case import UpdateDocumentRequest, UpdateDocumentUseCase

router = APIRouter()


@router.get(
    "/documents/{data_source_id}/{document_id}", operation_id="document_get_by_id", response_model=GetDocumentResponse
)
def get_by_id(
    data_source_id: str,
    document_id: str,
    ui_recipe: Optional[str] = None,
    attribute: Optional[str] = None,
    depth: conint(gt=-1, lt=1000) = 999,
    user: User = Depends(get_current_user),
):
    # Allow specification of absolute document ref in document_id
    id_list = document_id.split(".", 1)
    if len(id_list) >= 2 and attribute:
        raise ValueError(
            "An attribute was specified in both the 'attribute' parameter and the 'document_id' parameter."
            "Please provide a single attribute specification."
        )
    use_case = GetDocumentUseCase(user)
    response: GetDocumentResponse = use_case.execute(
        GetDocumentRequest(
            data_source_id=data_source_id,
            document_id=id_list[0],
            ui_recipe=ui_recipe,
            attribute=attribute if len(id_list) == 1 else id_list[1],
            depth=depth,
        )
    )
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.get(
    "/documents-by-path/{data_source_id}",
    operation_id="document_get_by_path",
    response_model=dict,
)
def get_by_path(
    data_source_id: str,
    ui_recipe: Optional[str] = None,
    attribute: Optional[str] = None,
    path: Optional[str] = None,
    user: User = Depends(get_current_user),
):
    """
    Get a document by it's path in the form "{dataSource}/{rootPackage}/{subPackage(s)?/{name}
    """
    use_case = GetDocumentByPathUseCase(user)
    response = use_case.execute(
        GetDocumentByPathRequest(data_source_id=data_source_id, path=path, ui_recipe=ui_recipe, attribute=attribute)
    )
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])


@router.put("/documents/{data_source_id}/{document_id}", operation_id="document_update")
def update(
    data_source_id: str,
    document_id: str,
    data: Json = Form(...),
    attribute: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None),
    update_uncontained: Optional[bool] = False,
    user: User = Depends(get_current_user),
):
    update_use_case = UpdateDocumentUseCase(user)
    response = update_use_case.execute(
        UpdateDocumentRequest(
            data_source_id=data_source_id,
            data=data,
            document_id=document_id,
            attribute=attribute,
            files=files,
            update_uncontained=update_uncontained,
        )
    )
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
