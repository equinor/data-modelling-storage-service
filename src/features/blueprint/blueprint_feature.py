from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses
from restful.request_types.shared import common_type_constrained_string

from .use_cases.get_blueprint_use_case import (
    GetBlueprintResponse,
    get_blueprint_use_case,
)
from .use_cases.resolve_blueprint_use_case import resolve_blueprint_use_case

router = APIRouter(tags=["default", "blueprint"])


@router.get(
    "/blueprint/{type_ref:path}",
    operation_id="blueprint_get",
    response_model=GetBlueprintResponse,
    responses=responses,
)
@create_response(JSONResponse)
def get_blueprint(
    type_ref: common_type_constrained_string, context: str | None = None, user: User = Depends(auth_w_jwt_or_pat)
):
    """
    Fetch the Blueprint and Recipes from a type reference (including inherited attributes).

    - **type_ref**: <protocol>://<data_source>/<path_to_blueprint>
    - **context**: name of application that has Ui-/StorageRecipe lookup table (optional attribute)
    """
    return get_blueprint_use_case(type_ref, context, user)


@router.get("/resolve-path/{address:path}", operation_id="blueprint_resolve", response_model=str, responses=responses)
@create_response(PlainTextResponse)
def resolve_blueprint_id(address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Resolve address of a blueprint to its type path.

    - **address**: <data_source</<blueprint_uuid>
    """
    return resolve_blueprint_use_case(user=user, address=address)
