from typing import List

from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses

from .use_cases.search_use_case import SearchRequest, search_use_case

router = APIRouter(tags=["default", "search"], prefix="/search")


@router.post("", operation_id="search", response_model=dict, responses=responses)
@create_response(JSONResponse)
def search(
    data: dict,
    data_sources: List[str] = Query([]),
    sort_by_attribute: str = "name",
    user: User = Depends(auth_w_jwt_or_pat),
):
    """
    Takes a list of data source id's as a query parameter, and search those data sources for the posted dictionary.
    If data source list is empty, search all databases.

    - **data**: a JSON document, must include a "type" attribute. Can also include other attributes like "name".
    - **data_sources**: List of data sources to search in.
    - **sort_by_attribute**: which attribute to sort the result by

    """
    return search_use_case(
        user=user, request=SearchRequest(data_sources=data_sources, data=data, dotted_attribute_path=sort_by_attribute)
    )
