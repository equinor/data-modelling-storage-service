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
    """Search for Entities of a Specific Blueprint Type in the Provided Data Sources. 
    
    This endpoint searches the provided data sources for entities that match the search data object provided.
    It will return all the entities in database of the type specified, with attributes that match the requirements set in the search query.  

    Args: 
        data (dict): A dictionary containing a "type"-attribute which will be used to search . Other attributes can be used to filter the search. 
            Example: 
            {
                "type": "dmss://blueprints/root_package/ValuesBlueprint",
                "attribute_greater_than_example": ">100",
                "attribute_less_than_example": "<11".
                "my_string": "de" # will return entities with attributes of type "my_string" that starts with "de"
            }
            data_sources (List[str]): Optional list of data source id's of which to search. If left empty it will search all available databases. 
        sort_by_attribute (str): Optional attribute of which to sort the results. Default is "name". 
        user (User): The authenticated user accessing the endpoint.

    Returns: 
        dict: The sorted search results. 
    """
    return search_use_case(
        user=user, request=SearchRequest(data_sources=data_sources, data=data, dotted_attribute_path=sort_by_attribute)
    )
