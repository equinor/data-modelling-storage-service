from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.get_blueprint_use_case import get_blueprint_use_case
from .use_cases.resolve_blueprint_use_case import resolve_blueprint_use_case

router = APIRouter(tags=["default", "blueprint"])


@router.get("/blueprint/{type_ref:path}", operation_id="blueprint_get", response_model=dict, responses=responses)
@create_response(JSONResponse)
def get_blueprint(type_ref: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Fetch the Blueprint of a type (including inherited attributes)
    """
    return get_blueprint_use_case(user=user, entity_type=type_ref)


@router.get(
    "/resolve-path/{absolute_id:path}", operation_id="blueprint_resolve", response_model=str, responses=responses
)
@create_response(PlainTextResponse)
def resolve_blueprint_id(absolute_id: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Resolve the data_source/uuid form of a blueprint to its type path
    """
    return resolve_blueprint_use_case(user=user, absolute_id=absolute_id)
