from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4
from pydantic import BaseModel, UUID4


class AccessLevel(Enum):
    WRITE = 2
    READ = 1
    NONE = 0

    def check_privilege(self, required_level: "AccessLevel") -> bool:
        if self.value >= required_level.value:
            return True

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, cls):
            return v
        try:
            return cls[v]
        except KeyError:
            raise ValueError("invalid AccessLevel enum value ")


class User(BaseModel):
    username_id: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    roles: List[str] = []
    scope: AccessLevel = AccessLevel.WRITE


class ACL(BaseModel):
    """
    acl:
      owner: 'username_id'
      roles:
        'role': WRITE
      users:
        'username_id': WRITE
      others: READ
    """

    owner: str
    roles: Dict[str, AccessLevel] = {}
    users: Dict[str, AccessLevel] = {}
    others: AccessLevel = AccessLevel.READ

    def dict(self, **kwargs):
        return {
            "owner": self.owner,
            "roles": {k: v.name for k, v in self.roles.items()},
            "users": {k: v.name for k, v in self.users.items()},
            "others": self.others.name,
        }


class PATData(BaseModel):
    pat_hash: str = None
    uuid: UUID4 = str(uuid4())
    username_id: str
    # TODO: Roles should be checked on every request, as they mey be updated after the PAT has been created
    roles: List[str] = []
    scope: AccessLevel
    expire: datetime

    # TODO: It could be useful to have a 'name' or 'description' on the PAT
    def dict(self, *kwargs) -> dict:
        return {
            "_id": self.pat_hash,  # Use the actual hash as the indexed '_id' value, as this is looked up most often.
            "uuid": self.uuid,  # Another uuid is used to identify pat, which can safely be returned to user.
            "username_id": self.username_id,
            "roles": self.roles,
            "scope": self.scope.name,
            "expire": str(self.expire),
        }
