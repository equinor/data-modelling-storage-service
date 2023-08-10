from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses
from restful.request_types.shared import Entity, common_type_constrained_string

from .use_cases.instantiate_entity import instantiate_entity_use_case
from .use_cases.validate_entity import validate_entity_use_case
from .use_cases.validate_existing_entity import validate_existing_entity_use_case

router = APIRouter(tags=["default", "entity"], prefix="/entity")


@router.post("", operation_id="instantiate_entity", response_model=dict, responses=responses)
@create_response(JSONResponse)
def instantiate(entity: Entity, user: User = Depends(auth_w_jwt_or_pat)):
    """Create a new entity and return it.

    (entity is not saved in DMSS)
    Rules for instantiation:
    - all required attributes, as defined in the blueprint, are included.
      If the required attribute has a default value, that value will be used.
      If not, an 'empty' value will be used. For example empty string,
      an empty list, the number 0, etc.
    - optional attributes are not included (also true if optional attribute has a default value)
    """
    return instantiate_entity_use_case(basic_entity=entity, user=user)


@router.post("/validate", operation_id="validate_entity", responses=responses)
@create_response(JSONResponse)
def validate(
    entity: Entity, as_type: common_type_constrained_string | None = None, user: User = Depends(auth_w_jwt_or_pat)
):
    """Validate an entity.
    Will return detailed error messages and status code 422 if the entity is invalid.

    "as_type": Optional. Validate the root entity against this type instead of the one defined in the entity.
    """
    return validate_entity_use_case(entity=entity, as_type=as_type, user=user)


@router.post("/validate-existing-entity/{address:path}", operation_id="validate_existing_entity", responses=responses)
@create_response(JSONResponse)
def validate_existing(address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Validate an existing entity in dmss.
    Will return detailed error messages and status code 422 if an entity is invalid.

    """
    return validate_existing_entity_use_case(address=address, user=user)
