from pydantic.main import BaseModel

from common.utils.encryption import encrypt
from enums import StorageDataTypes


class Repository(BaseModel, use_enum_values=True):  # type: ignore
    type: str
    data_types: list[StorageDataTypes] | None = None
    host: str | None = None
    port: int | None = None
    username: str | None = None
    password: str | None = None
    database: str | None = None
    collection: str | None = None
    account_url: str | None = None  # URL to blob storage account, with SAS token included as a query parameter
    container: str | None = None
    tls: bool | None = True

    def to_dict(self) -> dict:
        return {
            **super().model_dump(),
            "password": encrypt(self.password) if self.password else None,
            "account_url": encrypt(self.account_url) if self.account_url else None,
        }


class DataSourceRequest(BaseModel):
    name: str
    repositories: dict[str, Repository]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "repositories": {k: v.to_dict() for k, v in self.repositories.items()},
        }
