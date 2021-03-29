from fastapi import APIRouter
from starlette.responses import JSONResponse

from api.core.use_case.search_use_case import SearchUseCase
from controllers.status_codes import STATUS_CODES

router = APIRouter()


@router.post("/search/{data_source_id}")
def search_entities(data_source_id: str, request: dict):
    use_case = SearchUseCase()
    request_object = {"data_source_id": data_source_id, "data": request}
    response = use_case.execute(request_object)
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
