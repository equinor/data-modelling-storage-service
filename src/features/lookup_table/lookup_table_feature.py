from fastapi import APIRouter, Depends
from starlette.responses import Response

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses
from features.lookup_table.use_cases.create_lookup_table import (
    create_lookup_table_use_case,
)

router = APIRouter(tags=["default", "lookup-table"])


@router.post(
    "/application/{application}",
    operation_id="create_lookup",
    status_code=204,
    response_class=Response,
    responses={**responses},
)
@create_response()
def create_lookup(recipe_package: str, application: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Create a recipe lookup table from a package containing RecipeLinks.
    Associate it with an application.
    This can be used for setting Ui- and StorageRecipes for specific applications.
    """
    return create_lookup_table_use_case(recipe_package, application, user)
