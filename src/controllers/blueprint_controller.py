from fastapi import APIRouter
from starlette.responses import Response

from restful.status_codes import STATUS_CODES
from use_case.get_blueprint import GetBlueprintUseCase

router = APIRouter()


@router.get("/blueprint/{type_ref:path}", operation_id="blueprint_get", response_model=dict)
def get_blueprint(type_ref: str):
    """
    Fetch the Blueprint of a type (including inherited attributes)
    """
    use_case = GetBlueprintUseCase()
    response = use_case.execute(type_ref)
    if not response.type == "SUCCESS":
        return Response(response.value, status_code=STATUS_CODES[response.type])
    return response.value
