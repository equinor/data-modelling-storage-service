from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses
from restful.request_types.shared import common_type_constrained_string

from .use_cases.instantiate_entity import BasicEntity, instantiate_entity_use_case
from .use_cases.validate_entity import validate_entity_use_case

router = APIRouter(tags=["default", "entity"], prefix="/entity")


@router.post("", operation_id="instantiate_entity", response_model=dict, responses=responses)
@create_response(JSONResponse)
def instantiate(entity: BasicEntity, user: User = Depends(auth_w_jwt_or_pat)):
    """Create a new entity and return it.

    (entity is not saved in DMSS)
    """
    return instantiate_entity_use_case(basic_entity=entity, user=user)


@router.post("/validate", operation_id="validate_entity", responses=responses)
@create_response(JSONResponse)
def validate(
    entity: BasicEntity, as_type: common_type_constrained_string | None = None, user: User = Depends(auth_w_jwt_or_pat)
):
    """Validate an entity.
    Will return detailed error messages and status code 422 if the entity is invalid.

    "as_type": Optional. Validate the root entity against this type instead of the one defined in the entity.
    """
    return validate_entity_use_case(entity=entity, as_type=as_type, user=user)
