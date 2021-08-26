from typing import Dict, List, Optional

from pydantic.main import BaseModel

from enums import RepositoryType, StorageDataTypes
from utils.encryption import encrypt


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

    def dict(self) -> dict:
        return {
            **{k: v for k, v in self},
            "password": encrypt(self.password) if self.password else None,
            "account_key": encrypt(self.account_key) if self.account_key else None,
        }


class DataSourceRequest(BaseModel):
    name: str
    repositories: Dict[str, Repository]

    def dict(self) -> dict:
        return {"name": self.name, "repositories": {k: v.dict() for k, v in self.repositories.items()}}
