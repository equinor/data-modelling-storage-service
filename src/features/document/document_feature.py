from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import Json, conint

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.add_document_to_path_use_case import add_document_to_path_use_case
from .use_cases.add_file_use_case import add_file_use_case
from .use_cases.add_raw_use_case import add_raw_use_case
from .use_cases.get_document_by_path_use_case import get_document_by_path_use_case
from .use_cases.get_document_use_case import get_document_use_case
from .use_cases.remove_by_path_use_case import remove_by_path_use_case
from .use_cases.remove_use_case import remove_use_case
from .use_cases.update_document_use_case import update_document_use_case

router = APIRouter(tags=["default", "document"], prefix="/documents")


@router.get(
    "/{data_source_id}/{document_id}", operation_id="document_get_by_id", response_model=dict, responses=responses
)
@create_response(JSONResponse)
def get_by_id(
    data_source_id: str,
    document_id: str,
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
    return get_document_use_case(
        user=user,
        document_id=id_list[0],
        data_source_id=data_source_id,
        attribute=attribute if len(id_list) == 1 else id_list[1],
        depth=depth,
    )


@router.get("-by-path/{data_source_id}", operation_id="document_get_by_path", response_model=dict, responses=responses)
@create_response(JSONResponse)
def get_by_path(
    data_source_id: str,
    attribute: Optional[str] = None,
    path: Optional[str] = None,
    user: User = Depends(auth_w_jwt_or_pat),
):
    """
    Get a document by it's path in the form "{dataSource}/{rootPackage}/{subPackage(s)?/{name}
    """
    return get_document_by_path_use_case(user=user, data_source_id=data_source_id, path=path, attribute=attribute)


@router.put("/{data_source_id}/{document_id}", operation_id="document_update", responses=responses)
@create_response(JSONResponse)
def update(
    data_source_id: str,
    document_id: str,
    data: Json = Form(...),
    attribute: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None),
    update_uncontained: Optional[bool] = False,
    user: User = Depends(auth_w_jwt_or_pat),
):

    return update_document_use_case(
        user=user,
        document_id=document_id,
        data_source_id=data_source_id,
        data=data,
        attribute=attribute,
        files=files,
        update_uncontained=update_uncontained,
    )


@router.delete(
    "/{data_source_id}/{dotted_id}", operation_id="document_remove", response_model=str, responses=responses
)
@create_response(PlainTextResponse)
def remove(data_source_id: str, dotted_id: str, user: User = Depends(auth_w_jwt_or_pat)):
    return remove_use_case(user=user, data_source_id=data_source_id, document_id=dotted_id)


@router.post(
    "/{data_source_id}/add-to-path", operation_id="document_add_to_path", response_model=dict, responses=responses
)
@create_response(JSONResponse)
def add_to_path(
    data_source_id: str,
    document: Json = Form(...),
    directory: str = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    update_uncontained: Optional[bool] = False,
    user: User = Depends(auth_w_jwt_or_pat),
):
    """
    Same as 'add_to_parent', but reference parent by path instead of ID. Also supports files.
    """
    return add_document_to_path_use_case(
        user=user,
        data_source_id=data_source_id,
        document=document,
        directory=directory,
        files=files,
        update_uncontained=update_uncontained,
    )


# TODO: Create test for this
@router.post("/{data_source_id}/add-raw", operation_id="document_add_simple", response_model=str, responses=responses)
@create_response(PlainTextResponse)
def add_raw(data_source_id: str, document: dict, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Adds the document 'as-is' to the datasource.
    NOTE: The 'explorer-add' operation is to be preferred.
    This is mainly for bootstrapping and imports.
    Blueprint need not exist, and so there is no validation or splitting of entities.
    Posted document must be a valid Entity.
    """
    return add_raw_use_case(user=user, document=document, data_source_id=data_source_id)


@router.post("/{absolute_ref:path}", operation_id="document_add", response_model=dict, responses=responses)
@create_response(JSONResponse)
def add_by_parent_id(
    absolute_ref: str,
    document: dict,
    update_uncontained: Optional[bool] = True,
    user: User = Depends(auth_w_jwt_or_pat),
):
    """
    Add a new document to absolute ref (root of data source, or another document).
    If added to another document, a valid attribute type check is done.
    Select parent with format 'data_source/document_id.attribute.index.attribute'
    """
    return add_file_use_case(
        user=user, absolute_ref=absolute_ref, data=document, update_uncontained=update_uncontained
    )


@router.post("/{data_source_id}/remove-by-path", operation_id="document_remove_by_path", responses=responses)
@create_response(PlainTextResponse)
def remove_by_path(data_source_id: str, directory: str, user: User = Depends(auth_w_jwt_or_pat)):
    return remove_by_path_use_case(user=user, data_source_id=data_source_id, directory=directory)
