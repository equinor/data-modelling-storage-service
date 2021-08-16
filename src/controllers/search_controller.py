from fastapi import APIRouter
from starlette.responses import JSONResponse

from restful.status_codes import STATUS_CODES
from use_case.search_use_case import SearchRequest, SearchUseCase

router = APIRouter()


@router.post("/search/{data_source_id}", operation_id="search", response_model=dict)
def search(data_source_id: str, request: dict, sort_by_attribute: str = "name"):
    use_case = SearchUseCase()
    response = use_case.execute(
        SearchRequest(data_source_id=data_source_id, data=request, sort_by_attribute=sort_by_attribute)
    )
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
