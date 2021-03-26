from typing import Dict, Optional

from pydantic.main import BaseModel

from api.core.enums import DataSourceType


class Repository(BaseModel, use_enum_values=True):
    type: DataSourceType
    name: str
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None
    collection: Optional[str] = None
    account_name: Optional[str] = None
    account_key: Optional[str] = None
    tls: Optional[bool] = True


class DataSourceRequest(BaseModel):
    name: str
    repositories: Dict[str, Repository]
