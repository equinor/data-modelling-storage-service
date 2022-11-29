from fastapi import APIRouter, Depends
from starlette.responses import Response

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses
from domain_classes.lookup import Lookup
from features.lookup_table.use_cases.create_lookup_table import create_lookup_table_use_case
from restful.request_types.shared import common_name_constrained_string

router = APIRouter(tags=["default", "lookup-table"], prefix="/lookup")


@router.post(
    "/{lookup_name:str}",
    operation_id="create_lookup",
    status_code=204,
    response_class=Response,
    responses={**responses},
)
@create_response()
def create_lookup(
    lookup_name: common_name_constrained_string, content: Lookup, user: User = Depends(auth_w_jwt_or_pat)
):
    """
    Create a named lookup table.
    This can be used for setting Ui- and StorageRecipes for specific applications.
    """
    return create_lookup_table_use_case(lookup_name, content, user)
