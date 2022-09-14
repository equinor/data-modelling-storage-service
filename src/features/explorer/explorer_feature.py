from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import Json

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.add_document_to_path_use_case import add_document_to_path_use_case
from .use_cases.add_file_use_case import add_file_use_case
from .use_cases.add_raw import add_raw_use_case
from .use_cases.remove_by_path_use_case import remove_by_path_use_case
from .use_cases.rename_file_use_case import rename_use_case

router = APIRouter(tags=["default", "explorer"], prefix="/explorer")


# TODO: Create test for this
@router.post("/{data_source_id}/add-raw", operation_id="explorer_add_simple", response_model=str, responses=responses)
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


# TODO: Create test for this
# TODO: DataSource is not needed in the path, as it's contained in the source and dest parameters
@router.post("/{data_source_id}/move", operation_id="explorer_move", response_model=str, responses=responses)
@create_response(PlainTextResponse)
def move(request_data, data_source_id: str, user: User = Depends(auth_w_jwt_or_pat)):  # noqa: E501
    raise NotImplementedError



@router.post("/{data_source_id}/remove-by-path", operation_id="explorer_remove_by_path", responses=responses)
@create_response(PlainTextResponse)
def remove_by_path(data_source_id: str, directory: str, user: User = Depends(auth_w_jwt_or_pat)):
    return remove_by_path_use_case(user=user, data_source_id=data_source_id, directory=directory)


@router.put("/{data_source_id}/rename", operation_id="explorer_rename", response_model=dict, responses=responses)
@create_response(JSONResponse)
def rename(
    data_source_id: str,
    document_id: str,
    parent_id: str,
    user: User = Depends(auth_w_jwt_or_pat),
):  # noqa: E501
    return rename_use_case(user=user, data_source_id=data_source_id, document_id=document_id, parent_id=parent_id)


@router.post(
    "/{data_source_id}/add-to-path", operation_id="explorer_add_to_path", response_model=dict, responses=responses
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


@router.post("/{absolute_ref:path}", operation_id="explorer_add", response_model=dict, responses=responses)
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
