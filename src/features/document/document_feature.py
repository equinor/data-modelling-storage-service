from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import Json, conint

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.address import Address
from common.providers.blueprint_provider import get_blueprint_provider
from common.providers.storage_recipe_provider import storage_recipe_provider
from common.responses import create_response, responses
from services.document_service.document_service import DocumentService
from storage.internal.data_source_repository import get_data_source

from .use_cases.add_document_use_case import add_document_use_case
from .use_cases.add_raw_use_case import add_raw_use_case
from .use_cases.check_exsistence_use_case import check_existence_use_case
from .use_cases.get_document_use_case import get_document_use_case
from .use_cases.remove_use_case import remove_use_case
from .use_cases.update_document_use_case import update_document_use_case

router = APIRouter(tags=["default", "document"], prefix="/documents")


@router.get(
    "/{address:path}",
    operation_id="document_get",
    response_model=dict,
    responses=responses,
)
@create_response(JSONResponse)
def get(
    address: str,
    depth: conint(gt=-1, lt=1000) = 0,  # type: ignore
    user: User = Depends(auth_w_jwt_or_pat),
):
    """Get a Document as JSON String

    This endpoint can be used for getting entities, blueprints or other json documents from the database.

    Args:
    - address: path address to where the document should be stored.
      - Example: Reference to data source: PROTOCOL://DATA SOURCE
      - Example: Reference to package by id: PROTOCOL://DATA SOURCE/$ID
      - Example: Reference to package by path: PROTOCOL://DATA SOURCE/ROOT PACKAGE/SUB PACKAGE
      - The PROTOCOL is optional, and the default is dmss.
    - document (dict): The document that is to be stored.
    - depth (int): The maximum depth for resolving nested documents.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - dict: The document requested.
    """
    return get_document_use_case(user=user, address=address, depth=depth)


@router.put("/{id_address:path}", operation_id="document_update", responses=responses)
@create_response(JSONResponse)
def update(
    id_address: str,
    data: Json = Form(...),
    files: list[UploadFile] | None = File(None),
    user: User = Depends(auth_w_jwt_or_pat),
):
    """Update an Existing Document in the Database.

    This endpoint can be used for updating an existing document

    Args:
    - address: Path address to the document that should be updated.
      - Example: Reference to data source: PROTOCOL://DATA SOURCE
      - Example: Reference to package by id: PROTOCOL://DATA SOURCE/$ID
      - Example: Reference to package by path: PROTOCOL://DATA SOURCE/ROOT PACKAGE/SUB PACKAGE
      - The PROTOCOL is optional, and the default is dmss.
    - document (dict): The document to replace the previous version.
    - files: Optional list of files to be stored as part of this document.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - dict: The updated document.
    """

    document_service = DocumentService(
        repository_provider=get_data_source,
        user=user,
        blueprint_provider=get_blueprint_provider(user),
        recipe_provider=storage_recipe_provider,
    )

    return update_document_use_case(
        address=Address.from_absolute(id_address),
        data=data,
        files=files,
        document_service=document_service,
    )


@router.post(
    "/{address:path}",
    operation_id="document_add",
    response_model=dict,
    responses=responses,
)
@create_response(JSONResponse)
def add_document(
    address: str,
    document: Json = Form(...),
    files: list[UploadFile] | None = File(None),
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
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - dict: A dictionary with one element, "uid", which is the ID of the created document.
    """
    #     TODO decide if we should support adding an empty list. That is currently not supported.

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
        document_service=document_service,
    )


# TODO: Create test for this
@router.post(
    "-add-raw/{data_source_id}",
    operation_id="document_add_simple",
    response_model=str,
    responses=responses,
)
@create_response(PlainTextResponse)
def add_raw(data_source_id: str, document: dict, user: User = Depends(auth_w_jwt_or_pat)):
    """Adding a document 'as-is' to the data source, mainly used for bootstrapping and imports.

    This endpoint adds a document to the data source, without any validation or splitting up of entities.
    A blueprint for the entity need not exist. Posted document must be a valid Entity, with a "type" defined.

    Args:
    - data_source_id (str): The ID of the data source where the document should be added.
    - document (dict): The document to add to the data source.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - str: ID of the document that was uploaded.
    """
    return add_raw_use_case(user=user, document=document, data_source_id=data_source_id)


@router.delete("/{address:path}", operation_id="document_remove", responses=responses)
@create_response(PlainTextResponse)
def remove(address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Remove a document from the database.

    Args:
    - address (str): path address to the document that is to be deleted.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - str: "OK" (200)
    """
    return remove_use_case(user=user, address=address)


@router.get(
    "-existence/{address:path}",
    operation_id="document_check",
    response_model=bool,
    responses=responses,
)
@create_response(JSONResponse)
def check_existence(address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Checks if an entity exists, given an address.

    Args:
    - Address

    Returns:
    - bool: 'true' if the address points to an existing document, else 'false'.
    """
    document_service = DocumentService(repository_provider=get_data_source, user=user)
    return check_existence_use_case(address=Address.from_absolute(address), document_service=document_service)
