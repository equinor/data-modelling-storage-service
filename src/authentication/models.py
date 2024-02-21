from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel

from config import config


class AccessLevel(str, Enum):
    WRITE = "WRITE"
    READ = "READ"
    NONE = "NONE"

    def check_privilege(self, required_level: "AccessLevel") -> bool:
        if self.value >= required_level.value:
            return True
        return False


class User(BaseModel):
    user_id: str  # If using azure AD authentication, user_id is the oid field from the access token.
    # If using another oauth provider, user_id will be from the "sub" attribute in the access token.
    email: str | None = None
    full_name: str | None = None
    roles: list[str] = []
    scope: AccessLevel = (
        AccessLevel.WRITE
    )  # This is the 'maximum' AccessLevel this user can have, but is not what is actually set as the access level.

    @classmethod
    def default(cls):
        return cls(user_id="nologin", full_name="Not Authenticated", email="nologin@example.com")

    def __hash__(self):
        return hash(self.user_id)


class AccessControlList(BaseModel):
    """
    acl:
      owner: 'user_id'
      roles:
        'role': WRITE
      users:
        'user_id': WRITE
      others: READ
    """

    owner: str
    roles: dict[str, AccessLevel] = {}
    users: dict[str, AccessLevel] = {}
    others: AccessLevel = AccessLevel.READ

    def to_dict(self, **kwargs):
        return {
            "owner": self.owner,
            "roles": {k: v.name for k, v in self.roles.items()},
            "users": {k: v.name for k, v in self.users.items()},
            "others": self.others.name,
        }

    @classmethod
    def default(cls):
        return cls(
            owner=config.DMSS_ADMIN,
            roles={config.DMSS_ADMIN_ROLE: AccessLevel.WRITE},
            others=AccessLevel.READ,
        )

    @classmethod
    def default_with_owner(cls, user: User):
        """Used when there is no ACL to inherit. Sets the current user as owner, and rest copies DEFAULT_ACL"""
        acl = cls.default()
        acl.owner = user.user_id
        return acl


class PATData(BaseModel):
    pat_hash: str | None = None
    uuid: str = str(uuid4())
    user_id: str
    # TODO: Roles should be checked on every request, as they mey be updated after the PAT has been created
    roles: list[str] = []
    scope: AccessLevel
    expire: datetime

    # TODO: It could be useful to have a 'name' or 'description' on the PAT
    def dict(self, *kwargs) -> dict:
        return {
            "_id": self.pat_hash,  # Use the actual hash as the indexed '_id' value, as this is looked up most often.
            "uuid": self.uuid,  # Another uuid is used to identify pat, which can safely be returned to user.
            "user_id": self.user_id,
            "roles": self.roles,
            "scope": self.scope.name,
            "expire": str(self.expire),
        }

    def is_expired(self):
        return datetime.now() > self.expire
