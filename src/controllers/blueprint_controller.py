from fastapi import APIRouter, Depends

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from use_case.get_blueprint import GetBlueprintUseCase
from use_case.resolve_blueprint import ResolveBlueprintUseCase

router = APIRouter()


@router.get("/blueprint/{type_ref:path}", operation_id="blueprint_get", response_model=dict)
def get_blueprint(type_ref: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Fetch the Blueprint of a type (including inherited attributes)
    """
    use_case = GetBlueprintUseCase(user)
    return use_case.execute(type_ref)


@router.get("/resolve-path/{absolute_id:path}", operation_id="blueprint_resolve", response_model=str)
def resolve_blueprint_id(absolute_id: str, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Resolve the data_source/uuid form of a blueprint to it's type path
    """
    return ResolveBlueprintUseCase(user).execute(absolute_id)
