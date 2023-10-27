from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.get_attribute_use_case import get_attribute_use_case

router = APIRouter(tags=["default", "attribute"], prefix="/attribute")


class GetAttributeResponse(BaseModel):
    attribute: dict
    address: str


@router.get(
    "/{address:path}",
    operation_id="attribute_get",
    response_model=GetAttributeResponse,
    responses=responses,
)
@create_response(JSONResponse)
def get_attribute(address: str, resolve: bool = True, user: User = Depends(auth_w_jwt_or_pat)):
    """Fetch the BlueprintAttribute which is the container for the addressed object.

    This endpoint is used for fetching a BlueprintAttribute in which the addressed entity is contained.

    Args:
    - address (str): The address to the entity.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - dict: The blueprint-attribute object.
    """
    return get_attribute_use_case(user=user, address=address, resolve=resolve)
