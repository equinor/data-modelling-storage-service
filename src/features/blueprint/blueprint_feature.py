from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses
from restful.request_types.shared import TypeConstrainedString

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
    type_ref: TypeConstrainedString,
    context: str | None = None,
    user: User = Depends(auth_w_jwt_or_pat),
):
    """Get a Blueprint and all Ui- and StorageRecipes connected to it, given a Blueprint address.

    Args:
    - type_ref (str): The address of the blueprint.
        - Example: PROTOCOL://<DATA-SOURCE>/<PACKAGE>/<FOLDER>/<NAME>
    - context (str): Optional name of application that has Ui-/StorageRecipe lookup table.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - GetBlueprintResponse: An object containing the blueprint, a list of all UI- recipes and a list of all StorageRecipes.
    """
    return get_blueprint_use_case(type_ref, context, user)


@router.get(
    "/resolve-path/{address:path}",
    operation_id="blueprint_resolve",
    response_model=str,
    responses=responses,
)
@create_response(PlainTextResponse)
def resolve_blueprint_id(address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Resolve path address of a blueprint given id address.

    This endpoint takes in an ID-address of a blueprint and finds the full path address to the blueprint.

    Args:
    - address (str): The ID address of the blueprint.
        - Example: PROTOCOL://<DATA-SOURCE>/$<UUID>

    Returns:
    - str: the path address of the blueprint.
        - Example:  PROTOCOL://<DATA-SOURCE>/<PACKAGE>/<FOLDER>/<NAME>
    """
    return resolve_blueprint_use_case(user=user, address=address)
