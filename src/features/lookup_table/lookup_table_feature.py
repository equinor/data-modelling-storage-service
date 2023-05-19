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
    """
    Create a recipe lookup table from a package containing RecipeLinks.
    Associate it with an application.
    This can be used for setting Ui- and StorageRecipes for specific applications.

    - **application**: name of application
    - **recipe_package**: List with one or more paths to package(s) that contain recipe links. (Example: 'system/SIMOS/recipe_links')
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
    """
    Fetch a single lookup table.

    - **application**: name of application
    """
    return get_lookup_table_use_case(application, user)
