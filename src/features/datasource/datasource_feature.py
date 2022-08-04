from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, PlainTextResponse

from common.responses import create_response

from authentication.authentication import auth_w_jwt_or_pat
from authentication.models import User
from restful.request_types.create_data_source import DataSourceRequest
from restful.request_types.shared import DataSource
from storage.internal.data_source_repository import DataSourceRepository

from .use_cases.create_data_source_use_case import CreateDataSourceRequest, CreateDataSourceUseCase
from .use_cases.get_data_source_use_case import GetDataSourceUseCase
from .use_cases.get_data_sources_use_case import GetDataSourcesUseCase

router = APIRouter(tags=["default", "datasource"], prefix="/data-sources")


@router.get("/{data_source_id}", operation_id="data_source_get", response_model=dict)
@create_response(JSONResponse)
def get(data_source_id: str, user: User = Depends(auth_w_jwt_or_pat)):
    data_source_repository = DataSourceRepository(user)
    use_case = GetDataSourceUseCase(data_source_repository)
    return use_case.execute(DataSource(data_source_id=data_source_id))


@router.post("/{data_source_id}", operation_id="data_source_save", response_model=str)
@create_response(PlainTextResponse)
def save(data_source_id: str, new_data_source: DataSourceRequest, user: User = Depends(auth_w_jwt_or_pat)):
    """
    Create or update a data source configuration
    """
    data_source_repository = DataSourceRepository(user)
    use_case = CreateDataSourceUseCase(data_source_repository=data_source_repository)
    return use_case.execute(CreateDataSourceRequest(data_source_id=data_source_id, new_data_source=new_data_source))


@router.get("", operation_id="data_source_get_all", response_model=list[dict])
@create_response(JSONResponse)
def get_all(user: User = Depends(auth_w_jwt_or_pat)):
    data_source_repository = DataSourceRepository(user)
    use_case = GetDataSourcesUseCase(data_source_repository)
    return use_case.execute()
