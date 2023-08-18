from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses
from restful.request_types.shared import Entity, TypeConstrainedString

from .use_cases.instantiate_entity import instantiate_entity_use_case
from .use_cases.validate_entity import validate_entity_use_case
from .use_cases.validate_existing_entity import validate_existing_entity_use_case

router = APIRouter(tags=["default", "entity"], prefix="/entity")


@router.post("", operation_id="instantiate_entity", response_model=dict, responses=responses)
@create_response(JSONResponse)
def instantiate(entity: Entity, user: User = Depends(auth_w_jwt_or_pat)):
    """Returns a default entity of specified type. This entity is not stored in the database.

    This endpoint creates a default entity of the specified type. A default entity of that type is
    specified to contain all the required fields with their default values. If no default value is set for the field,
    then an 'empty' value will be set for that field. For an int that would be 0, and for a string that would be "".
    Optional attributes are not filled in, even if a default value is specified for that optional field.

    Args:
    - entity (Entity): A JSON object with only a "type" parameter. Any other fields will be ignored.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - dict: A default entity of the specified type.
    """
    return instantiate_entity_use_case(basic_entity=entity, user=user)


@router.post("/validate", operation_id="validate_entity", responses=responses)
@create_response(JSONResponse)
def validate(entity: Entity, as_type: TypeConstrainedString | None = None, user: User = Depends(auth_w_jwt_or_pat)):
    """Validate an entity according to its blueprint.

    This endpoint compares the entity to the specifications of its blueprint. The entity's blueprint is specified
    as the 'type' parameter. The entity is required to have all attributes that are specified as required in the
    blueprint, and they must be on the correct format.

    This endpoint returns a detailed error messages and status code 422 if the entity is invalid.

    Args:
    - entity (Entity): a dict object with "type" specified.

    Returns:
    - str: "OK" (200)
    """
    return validate_entity_use_case(entity=entity, as_type=as_type, user=user)


@router.post("/validate-existing-entity/{address:path}", operation_id="validate_existing_entity", responses=responses)
@create_response(JSONResponse)
def validate_existing(address: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Validate an entity stored in the database according to its blueprint .

    This endpoint compares the entity to the specifications of its blueprint. The entity's blueprint is specified
    as the 'type' parameter. The entity is required to have all attributes that are specified as required in the
    blueprint, and they must be on the correct format.

    This endpoint returns a detailed error messages and status code 422 if the entity is invalid.

    Args:
    - address (str): address path to the entity that is to be validated.

    Returns:
    - str: "OK" (200)
    """
    return validate_existing_entity_use_case(address=address, user=user)
