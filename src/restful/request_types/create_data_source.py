from typing import Dict, List, Optional

from pydantic.main import BaseModel

from enums import RepositoryType, StorageDataTypes


class Repository(BaseModel, use_enum_values=True):
    type: RepositoryType
    data_types: Optional[List[StorageDataTypes]] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None
    collection: Optional[str] = None
    account_name: Optional[str] = None
    account_key: Optional[str] = None
    container: Optional[str] = None
    tls: Optional[bool] = True


class DataSourceRequest(BaseModel):
    name: str
    repositories: Dict[str, Repository]
