from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from common.responses import create_response

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from .use_cases.get_blueprint_use_case import GetBlueprintUseCase
from .use_cases.resolve_blueprint_use_case import ResolveBlueprintUseCase

router = APIRouter(tags=["default", "blueprint"])


@router.get("/blueprint/{type_ref:path}", operation_id="blueprint_get", response_model=dict)
@create_response(JSONResponse)
def get_blueprint(type_ref: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Fetch the Blueprint of a type (including inherited attributes)
    """
    use_case = GetBlueprintUseCase(user)
    return use_case.execute(type_ref)


@router.get("/resolve-path/{absolute_id:path}", operation_id="blueprint_resolve", response_model=str)
@create_response(PlainTextResponse)
def resolve_blueprint_id(absolute_id: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Resolve the data_source/uuid form of a blueprint to it's type path
    """
    use_case = ResolveBlueprintUseCase(user)
    return use_case.execute(absolute_id)
