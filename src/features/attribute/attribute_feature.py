from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.get_attribute_use_case import get_attribute_use_case

router = APIRouter(tags=["default", "attribute"], prefix="/attribute")


@router.get(
    "/{address:path}",
    operation_id="attribute_get",
    response_model=dict,
    responses=responses,
)
@create_response(JSONResponse)
def get_attribute(address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Fetch the attribute from a address.
    """
    return get_attribute_use_case(user=user, address=address)
