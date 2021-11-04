from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from authentication.authentication import get_current_user
from domain_classes.user import User
from restful.status_codes import STATUS_CODES
from use_case.search_use_case import SearchRequest, SearchUseCase

router = APIRouter()


@router.post("/search/{data_source_id}", operation_id="search", response_model=dict)
def search(
    data_source_id: str, request: dict, sort_by_attribute: str = "name", user: User = Depends(get_current_user)
):
    use_case = SearchUseCase(user)
    response = use_case.execute(
        SearchRequest(data_source_id=data_source_id, data=request, dotted_attribute_path=sort_by_attribute)
    )
    return JSONResponse(response.value, status_code=STATUS_CODES[response.type])
