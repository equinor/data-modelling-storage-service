from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse
from typing import List

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User

from common.responses import create_response

from .use_cases.search_use_case import SearchRequest, SearchUseCase

router = APIRouter(tags=["search"], prefix="/search")


@router.post("", operation_id="search", response_model=dict)
@create_response(JSONResponse)
def search(
    request: dict,
    data_sources: List[str] = Query([]),
    sort_by_attribute: str = "name",
    user: User = Depends(auth_w_jwt_or_pat),
):
    """
    Takes a list of data source id's as a query parameter, and search all data sources for the posted dictionary.
    If data source list is empty, search all databases.
    """
    use_case = SearchUseCase(user)
    return use_case.execute(
        SearchRequest(data_sources=data_sources, data=request, dotted_attribute_path=sort_by_attribute)
    )
