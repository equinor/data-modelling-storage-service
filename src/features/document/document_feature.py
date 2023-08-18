from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import Json, conint

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.add_document_use_case import add_document_use_case
from .use_cases.add_raw_use_case import add_raw_use_case
from .use_cases.get_document_use_case import get_document_use_case
from .use_cases.remove_use_case import remove_use_case
from .use_cases.update_document_use_case import update_document_use_case

router = APIRouter(tags=["default", "document"], prefix="/documents")


@router.get("/{address:path}", operation_id="document_get", response_model=dict, responses=responses)
@create_response(JSONResponse)
def get(
    address: str,
    depth: conint(gt=-1, lt=1000) = 1,  # type: ignore
    user: User = Depends(auth_w_jwt_or_pat),
):
    """
    Get document as JSON string.

    - **address**: An address to a package or a data source
      - By id: PROTOCOL://DATA SOURCE/$ID.Attribute
      - By path: PROTOCOL://DATA SOURCE/ROOT PACKAGE/SUB PACKAGE/ENTITY.Attribute
      - By query: PROTOCOL://DATA SOURCE/$ID.list(key=value)

    The PROTOCOL is optional, and the default is dmss.

    - **depth**: Maximum depth for resolving nested documents.
    """
    return get_document_use_case(user=user, address=address, depth=depth)


@router.put("/{id_address:path}", operation_id="document_update", responses=responses)
@create_response(JSONResponse)
def update(
    id_address: str,
    data: Json = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    update_uncontained: Optional[bool] = False,
    user: User = Depends(auth_w_jwt_or_pat),
):
    """Update document
    - **id_address**: <protocol>://<data_source>/$<document_uuid> (can also include an optional .<attribute> after <document_uuid>)
    """
    return update_document_use_case(
        user=user,
        address=id_address,
        data=data,
        files=files,
        update_uncontained=update_uncontained,
    )


@router.post("/{address:path}", operation_id="document_add", response_model=dict, responses=responses)
@create_response(JSONResponse)
def add_document(
    address: str,
    document: Json = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    update_uncontained: Optional[bool] = False,
    user: User = Depends(auth_w_jwt_or_pat),
):
    """Add a document to a package or a data source using an address.

    This endpoint can be used for:
    - Adding a new document to a package / data source.
    - Adding an object to an entity (for example filling in an optional, complex attribute)
    - Adding elements to a list attribute in an entity.

    Args:
    - address: path address to where the document should be stored.
      - Example: Reference to data source: PROTOCOL://DATA SOURCE
      - Example: Reference to package by id: PROTOCOL://DATA SOURCE/$ID
      - Example: Reference to package by path: PROTOCOL://DATA SOURCE/ROOT PACKAGE/SUB PACKAGE
      - The PROTOCOL is optional, and the default is dmss.
    - document (dict): The document that is to be stored.
    - files: Optional list of files to be stored as part of this document.
    - update_uncontained (bool): Optional flag specifying whether
    - user (User): The authenticated user accessing the endpoint.


    """
    return add_document_use_case(
        user=user,
        address=address,
        document=document,
        files=files,
        update_uncontained=update_uncontained,
    )


# TODO: Create test for this
@router.post("-add-raw/{data_source_id}", operation_id="document_add_simple", response_model=str, responses=responses)
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


@router.delete("/{address:path}", operation_id="document_remove", responses=responses)
@create_response(PlainTextResponse)
def remove(address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Remove a document from the database.

    Args:
    - address (str): path address to the document that is to be deleted.

    Returns:
    - str: "OK" (200)
    """
    return remove_use_case(user=user, address=address)
