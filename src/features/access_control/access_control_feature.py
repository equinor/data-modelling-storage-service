from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import AccessControlList, User
from common.responses import create_response, responses
from common.utils.get_blueprint import get_blueprint_provider
from common.utils.get_storage_recipe import storage_recipe_provider
from services.document_service import DocumentService
from storage.internal.data_source_repository import (
    DataSourceRepository,
    get_data_source,
)

from .use_cases.get_acl_use_case import get_acl_use_case
from .use_cases.set_acl_use_case import set_acl_use_case

router = APIRouter(tags=["default", "access_control"], prefix="/acl")


@router.put("/{data_source_id}/{document_id}", operation_id="set_acl", response_model=str, responses=responses)
@create_response(PlainTextResponse)
def set_acl(
    data_source_id: str,
    document_id: str,
    acl: AccessControlList,
    recursively: bool = True,
    user: User = Depends(auth_w_jwt_or_pat),
):
    """Update access control list (ACL) for a document.

    Args:
    - data_source_id (str): The ID of the data source which the document resides in.
    - document_id (str): The ID of the document for which to set the ACL.
    - acl (ACL): An access control list.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - str: "OK" (200)
    """
    document_service = DocumentService(
        repository_provider=get_data_source,
        user=user,
        blueprint_provider=get_blueprint_provider(user),
        recipe_provider=storage_recipe_provider,
    )

    return set_acl_use_case(
        data_source_id=data_source_id,
        document_id=document_id,
        acl=acl,
        recursively=recursively,
        data_source_repository=DataSourceRepository(user),
        document_service=document_service,
    )


@router.get(
    "/{data_source_id}/{document_id}", operation_id="get_acl", response_model=AccessControlList, responses=responses
)
@create_response(JSONResponse)
def get_acl(data_source_id: str, document_id: str, user: User = Depends(auth_w_jwt_or_pat)):
    """GET the access control list (ACL) for a document.

    The ACL determines which access a given user has for a document (Read, Write or None).

    Args:
    - data_source_id (str): The ID of the data source which the document resides in.
    - document_id (str): The ID of the document for which to check the ACL.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - ACL: The access control list requested.
    """
    return get_acl_use_case(
        data_source_id=data_source_id, document_id=document_id, data_source_repository=DataSourceRepository(user)
    ).dict()
