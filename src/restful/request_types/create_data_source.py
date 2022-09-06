from typing import Dict, List, Optional

from pydantic.main import BaseModel

from common.utils.encryption import encrypt
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
    account_url: Optional[str] = None  # URL to blob storage account, with SAS token included as a query parameter
    container: Optional[str] = None
    tls: Optional[bool] = True

    def dict(self) -> dict:
        return {
            **{k: v for k, v in self},
            "password": encrypt(self.password) if self.password else None,
            "account_url": encrypt(self.account_url) if self.account_url else None,
        }


class DataSourceRequest(BaseModel):
    name: str
    repositories: Dict[str, Repository]

    def dict(self) -> dict:
        return {"name": self.name, "repositories": {k: v.dict() for k, v in self.repositories.items()}}
