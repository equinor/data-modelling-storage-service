from abc import ABC, abstractmethod

from pydantic import UUID4

from authentication.models import AccessControlList, User
from domain_classes.document_look_up import DocumentLookUp
from domain_classes.repository import Repository
from domain_classes.storage_recipe import StorageAttribute
from enums import StorageDataTypes


class DataSource(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls, a_dict, user: User):
        ...

    @abstractmethod
    def _get_repo_from_storage_attribute(self, storage_attribute: StorageAttribute = None, strict=False) -> Repository:
        ...

    @abstractmethod
    def get_default_repository(self) -> Repository:
        ...

    @abstractmethod
    def _lookup(self, document_id) -> DocumentLookUp:
        ...

    @abstractmethod
    def get_storage_affinity(self, document_id) -> StorageDataTypes:
        ...

    @abstractmethod
    def _update_lookup(self, lookup: DocumentLookUp):
        ...

    @abstractmethod
    def update_access_control(self, document_id: str, acl: AccessControlList) -> None:
        ...

    @abstractmethod
    def get_lookup(self, document_id: str) -> DocumentLookUp:
        ...

    @abstractmethod
    def _remove_lookup(self, lookup_id):
        ...

    @abstractmethod
    def get(self, uid: str | UUID4) -> dict:
        ...

    @abstractmethod
    def find(self, filter: dict) -> list[dict]:
        ...

    @abstractmethod
    def update(
        self, document: dict, storage_attribute: StorageAttribute = None, parent_id: str | None = None, **kwargs
    ) -> None:
        ...

    @abstractmethod
    def update_blob(self, uid: str, filename: str, content_type: str, file) -> None:
        ...

    @abstractmethod
    def get_blob(self, uid: str) -> bytes:
        ...

    @abstractmethod
    def delete_blob(self, uid: str) -> None:
        ...

    @abstractmethod
    def delete(self, uid: str) -> None:
        ...
