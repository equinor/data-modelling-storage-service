from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.instantiate_entity import BasicEntity, instantiate_entity_use_case

router = APIRouter(tags=["default", "entity"], prefix="/entity")


@router.post("", operation_id="instantiate_entity", response_model=dict, responses=responses)
@create_response(JSONResponse)
def instantiate(entity: BasicEntity, user: User = Depends(auth_w_jwt_or_pat)):
    return instantiate_entity_use_case(basic_entity=entity, user=user)
