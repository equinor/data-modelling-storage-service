from dataclasses import dataclass
from functools import lru_cache

from pydantic import UUID4

from authentication.access_control import assert_user_has_access
from authentication.models import AccessControlList, User, AccessLevel
from config import config
from domain_classes.document_look_up import DocumentLookUp
from storage.data_source_class import DataSource
from storage.internal.data_source_repository import get_data_source_cached


@dataclass
class AuthStorageWrapper:
    acl: AccessControlList = AccessControlList.default()

    def update_access_control(self, document_id: str, acl: AccessControlList) -> None:
        ...

    @lru_cache(maxsize=config.CACHE_MAX_SIZE)
    def _get_cached(self, uid: str | UUID4, data_source_id: str) -> (dict, DocumentLookUp):
        data_source = get_data_source_cached(data_source_id)
        return data_source.get(uid)

    def get(self, uid: str | UUID4, data_source_id: str, user: User) -> dict:
        document, lookup = self._get_cached(uid, data_source_id)
        assert_user_has_access(lookup.acl, AccessLevel.READ, user)
        return document

prod_storage_wrapper = AuthStorageWrapper()

@dataclass
class WrapperWrapper(DataSource):
    user: User

    def get(self, *args, **kwargs):
        return prod_storage_wrapper.get(*args, **kwargs, user=self.user)


