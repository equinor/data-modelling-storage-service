from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import Json, conint

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.address import Address
from common.responses import create_response, responses
from common.utils.get_blueprint import get_blueprint_provider
from common.utils.get_storage_recipe import storage_recipe_provider
from services.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source

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
    """
    Add a document to a package (or a data source) using an address.

    - **address**:
      - Reference to data source: PROTOCOL://DATA SOURCE
      - Reference to package by id: PROTOCOL://DATA SOURCE/$ID
      - Reference to package by path: PROTOCOL://DATA SOURCE/ROOT PACKAGE/SUB PACKAGE
      The PROTOCOL is optional, and the default is dmss.

    This endpoint can be used for:
    - Adding elements to a list attribute in an entity.
    - Adding a new document to a package / data source
    - Adding an object to an entity (for example filling in an optional, complex attribute)
    """

    document_service = DocumentService(
        repository_provider=get_data_source,
        user=user,
        blueprint_provider=get_blueprint_provider(user),
        recipe_provider=storage_recipe_provider,
    )

    return add_document_use_case(
        address=Address.from_absolute(address),
        document=document,
        files=files,
        update_uncontained=update_uncontained,
        document_service=document_service,
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
    """Remove a document from DMSS."""
    return remove_use_case(user=user, address=address)
