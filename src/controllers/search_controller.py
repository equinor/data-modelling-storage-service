from fastapi import APIRouter, Depends, Query
from typing import List
from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from use_case.search_use_case import SearchRequest, SearchUseCase

router = APIRouter()


# remove data source id from url and use a list as query param.
# should take in a list of data sources instead of a single. If list is empty, search all datasources.
# searching multiple mongo repositories should happen in paralel if possible



# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#query-parameter-list-multiple-values


@router.post("/search/", operation_id="search", response_model=dict)
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
