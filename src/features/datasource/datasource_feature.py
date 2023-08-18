from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from common.responses import create_response, responses
from restful.request_types.create_data_source import DataSourceRequest
from restful.request_types.shared import DataSource
from storage.internal.data_source_repository import (
    DataSourceInformation,
    DataSourceRepository,
)

from .use_cases.create_data_source_use_case import create_data_source_use_case
from .use_cases.get_data_source_use_case import get_data_source_use_case
from .use_cases.get_data_sources_use_case import get_data_sources_use_case

router = APIRouter(tags=["default", "datasource"], prefix="/data-sources")


@router.get("/{data_source_id}", operation_id="data_source_get", response_model=dict, responses=responses)
@create_response(JSONResponse)
def get(data_source_id: str, user: User = Depends(auth_w_jwt_or_pat)):
    """Get configuration of a single data source.

    Args:
    - data_source_id (str): ID of the data source
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - dict: A dictionary containing configuration for the specified data source.
    """
    data_source_repository = DataSourceRepository(user)
    return get_data_source_use_case(
        data_source_repository=data_source_repository, data_source=DataSource(data_source_id=data_source_id)
    )


@router.post("/{data_source_id}", operation_id="data_source_save", response_model=str, responses=responses)
@create_response(PlainTextResponse)
def save(
    data_source_id: str,
    new_data_source: DataSourceRequest,
    user: User = Depends(auth_w_jwt_or_pat),
):
    """Create or update a data source configuration.

    This endpoint is used for creating or updating a data source configuration.
    A data source can have multiple repositories.

    Args:
    - data_source_id (str): ID of the data source
    - new_data_source (DataSourceRequest): A dict object with keys "name" and "repositories" which is another dict of
    str and repository configuration. This is the config of the data source.
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.


    Returns:
    - str: The ID of the newly created or updated data source.
    """
    data_source_repository = DataSourceRepository(user)
    return create_data_source_use_case(
        data_source_id=data_source_id, data_source_repository=data_source_repository, new_data_source=new_data_source
    )


@router.get("", operation_id="data_source_get_all", response_model=list[DataSourceInformation], responses=responses)
@create_response(JSONResponse)
def get_all(user: User = Depends(auth_w_jwt_or_pat)):
    """Get list of all data sources found in DMSS.

    Args:
    - user (User): The authenticated user accessing the endpoint, automatically generated from provided bearer token or Access-Key.

    Returns:
    - list (DataSourceInformation): A list of information about each data source found in the DMSS protocol.
    """
    data_source_repository = DataSourceRepository(user)
    return get_data_sources_use_case(data_source_repository=data_source_repository)
