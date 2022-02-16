from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import conint, Json

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from use_case.get_document_by_path_use_case import GetDocumentByPathRequest, GetDocumentByPathUseCase
from use_case.get_document_use_case import GetDocumentRequest, GetDocumentUseCase
from use_case.update_document_use_case import UpdateDocumentRequest, UpdateDocumentUseCase

router = APIRouter()


@router.get("/documents/{data_source_id}/{document_id}", operation_id="document_get_by_id", response_model=dict)
def get_by_id(
    data_source_id: str,
    document_id: str,
    ui_recipe: Optional[str] = None,
    attribute: Optional[str] = None,
    depth: conint(gt=-1, lt=1000) = 999,
    user: User = Depends(auth_w_jwt_or_pat),
):
    # Allow specification of absolute document ref in document_id
    id_list = document_id.split(".", 1)
    if len(id_list) >= 2 and attribute:
        raise ValueError(
            "An attribute was specified in both the 'attribute' parameter and the 'document_id' parameter."
            "Please provide a single attribute specification."
        )
    use_case = GetDocumentUseCase(user)
    return use_case.execute(
        GetDocumentRequest(
            data_source_id=data_source_id,
            document_id=id_list[0],
            ui_recipe=ui_recipe,
            attribute=attribute if len(id_list) == 1 else id_list[1],
            depth=depth,
        )
    )


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
    user: User = Depends(auth_w_jwt_or_pat),
):
    """
    Get a document by it's path in the form "{dataSource}/{rootPackage}/{subPackage(s)?/{name}
    """
    use_case = GetDocumentByPathUseCase(user)
    return use_case.execute(
        GetDocumentByPathRequest(data_source_id=data_source_id, path=path, ui_recipe=ui_recipe, attribute=attribute)
    )


@router.put("/documents/{data_source_id}/{document_id}", operation_id="document_update")
def update(
    data_source_id: str,
    document_id: str,
    data: Json = Form(...),
    attribute: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None),
    update_uncontained: Optional[bool] = False,
    user: User = Depends(auth_w_jwt_or_pat),
):
    update_use_case = UpdateDocumentUseCase(user)
    return update_use_case.execute(
        UpdateDocumentRequest(
            data_source_id=data_source_id,
            data=data,
            document_id=document_id,
            attribute=attribute,
            files=files,
            update_uncontained=update_uncontained,
        )
    )
