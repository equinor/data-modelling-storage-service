from enum import Enum
from typing import Dict

from pydantic import BaseModel

from domain_classes.user import User
from config import config
from utils.exceptions import MissingPrivilegeException


class AccessLevel(Enum):
    WRITE = 2
    READ = 1
    NONE = 0

    def check_privilege(self, required_level) -> bool:
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


class ACL(BaseModel):
    """
    acl:
      owner: 'username'
      roles:
        'role': WRITE
      users:
        'username': WRITE
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


def access_control(acl: ACL, access_level_required: AccessLevel, user: User):
    if not config.AUTH_ENABLED:
        return True

    # Starting with the 'others' access level should reduce the amount of checks being done the most
    if acl.others.check_privilege(access_level_required):
        return True
    # The owner always has full access
    if acl.owner == user.username:
        return True

    for role in user.roles:
        if role_access := acl.roles.get(role):
            if role_access.check_privilege(access_level_required):
                return True

    if direct_user_access := acl.users.get(user.username):
        if direct_user_access.check_privilege(access_level_required):
            return True

    # No access high enough granted neither as 'owner', 'roles', 'users', nor 'others'.
    raise MissingPrivilegeException(f"The requested operation requires '{access_level_required.name}' privileges")


def create_acl(user: User) -> ACL:
    """Used when there is no ACL to inherit. Sets the current user as owner, and rest copies DEFAULT_ACL"""
    return ACL(owner=user.username, roles=DEFAULT_ACL.roles, others=DEFAULT_ACL.others)


DEFAULT_ACL = ACL(owner=config.DMSS_ADMIN, roles={config.DMSS_ADMIN_ROLE: AccessLevel.WRITE}, others=AccessLevel.READ)
