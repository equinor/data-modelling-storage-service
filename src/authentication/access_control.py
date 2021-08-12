from enum import Enum
from typing import Dict

from pydantic import BaseModel

from authentication import authentication
from authentication.authentication import User
from authentication.mock_users import fake_users_db
from config import config
from utils.exceptions import MissingPrivilegeException


def current_user() -> User:
    if config.AUTH_ENABLED:
        if not authentication.user_context:
            raise Exception("No current user in user_context")
        return authentication.user_context
    return User(**fake_users_db["nologin"])


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


def access_control(acl: ACL, access_level_required: AccessLevel):
    user = current_user()

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


def create_acl(extra=None) -> ACL:
    user = current_user()
    return ACL(owner=user.username)
