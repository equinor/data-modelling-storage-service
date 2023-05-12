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
from .use_cases.get_document_use_case import get_document_use_case
from .use_cases.remove_by_path_use_case import remove_by_path_use_case
from .use_cases.remove_use_case import remove_use_case
from .use_cases.update_document_use_case import update_document_use_case

router = APIRouter(tags=["default", "document"], prefix="/documents")


@router.get("/{reference:path}", operation_id="document_get", response_model=dict, responses=responses)
@create_response(JSONResponse)
def get(
    reference: str,
    depth: conint(gt=-1, lt=1000) = 0,  # type: ignore
    resolve_links: bool = False,
    user: User = Depends(auth_w_jwt_or_pat),
):
    """
    Get document as JSON string.

    - **reference**:
      - By id: PROTOCOL://DATA SOURCE/$ID.Attribute
      - By path: PROTOCOL://DATA SOURCE/ROOT PACKAGE/SUB PACKAGE/ENTITY.Attribute
      - By query: PROTOCOL://DATA SOURCE/$ID.list(key=value)

      The PROTOCOL is optional, and the default is dmss.

    - **depth**: Maximum depth for resolving nested documents.
    """
    return get_document_use_case(user=user, reference=reference, depth=depth, resolve_links=resolve_links)


@router.put("/{id_reference:path}", operation_id="document_update", responses=responses)
@create_response(JSONResponse)
def update(
    id_reference: str,
    data: Json = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    user: User = Depends(auth_w_jwt_or_pat),
):
    """Update document
    - **id_reference**: <data_source>/<document_uuid> (can also include an optional .<attribute> after <document_uuid>)
    """
    return update_document_use_case(
        user=user,
        id_reference=id_reference,
        data=data,
        files=files,
    )


@router.delete("/{id_reference:path}", operation_id="document_remove", response_model=str, responses=responses)
@create_response(PlainTextResponse)
def remove(id_reference: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Remove document
    - **id_reference**: <data_source>/<document_uuid>.<attribute_path>

    Example: id_reference=SomeDataSource/3978d9ca-2d7a-4b47-8fed-57710f6cf50b.attributes.1 will remove the first element
    in the attribute list of a blueprint with the given id in data source 'SomeDataSource'.
    """
    return remove_use_case(user=user, id_reference=id_reference)


@router.post(
    "-by-path/{path_reference:path}", operation_id="document_add_to_path", response_model=dict, responses=responses
)
@create_response(JSONResponse)
def add_to_path(
    path_reference: str,
    document: Json = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    update_uncontained: Optional[bool] = False,
    user: User = Depends(auth_w_jwt_or_pat),
):
    """
    Same as 'add_to_parent', but reference parent by path instead of ID. Also supports files.

    - **path_reference**: <data_source>/<path_to_entity>/<entity_name>.<attribute>
    """
    return add_document_to_path_use_case(
        user=user,
        path_reference=path_reference,
        document=document,
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
    update_uncontained: bool = True,
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


@router.delete("-by-path/{path_reference:path}", operation_id="document_remove_by_path", responses=responses)
@create_response(PlainTextResponse)
def remove_by_path(path_reference: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Remove a document from DMSS.

    - **path_reference**: <data_source>/<path>.<attribute>
    """
    return remove_by_path_use_case(user=user, absolute_path=path_reference)
