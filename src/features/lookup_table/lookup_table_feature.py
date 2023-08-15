from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse, Response

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses
from domain_classes.lookup import Lookup
from features.lookup_table.use_cases.create_lookup_table import (
    create_lookup_table_use_case,
)
from features.lookup_table.use_cases.get_lookup_table import get_lookup_table_use_case

router = APIRouter(tags=["default", "lookup-table"])


@router.post(
    "/application/{application}",
    operation_id="create_lookup",
    status_code=204,
    response_class=Response,
    responses={**responses},
)
@create_response()
def create_lookup(application: str, recipe_package: list[str] = Query(), user: User = Depends(auth_w_jwt_or_pat)):
    """Creates a Recipe Lookup Table for an Application, given a Package Containing RecipeLinks.

    This endpoint creates a lookup table for an application. This lookup table is used to find UI- and Storage recipes given a blueprint.
    This recipe is associated with an application, based on application name.

    Args:
        application (str): Name of an application.
        recipe_package (list[str]): A list of one or more paths to packages that contain recipe links.
            Example: ["system/SIMOS/recipe_links"]
        user (User): The authenticated user accessing the endpoint.

    Returns:
        None, with status Code 204 (No Content).
    """
    return create_lookup_table_use_case(recipe_package, application, user)


@router.get(
    "/application/{application}",
    operation_id="get_lookup",
    response_model=Lookup,
    responses={**responses},
)
@create_response(JSONResponse)
def get_lookup(application: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Get The Lookup Table for UI- and Storage Recipes the Provided Application

    This endpoint fetches the recipe lookup table for the application provided.
    This lookup table is used to find UI- and Storage recipes given a blueprint.

    Args:
        application (str): The name of the desired application.

    Returns:
        dict: The recipe lookup table for the provided application.
    """
    return get_lookup_table_use_case(application, user)
