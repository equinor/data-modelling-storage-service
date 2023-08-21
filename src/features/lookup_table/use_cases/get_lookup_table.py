from authentication.access_control import (
    DEFAULT_ACCESS_CONTROL_LIST,
    assert_user_has_access,
)
from authentication.models import AccessLevel, User
from storage.internal.lookup_tables import get_lookup


def get_lookup_table_use_case(lookup_id: str, user: User) -> dict:
    assert_user_has_access(DEFAULT_ACCESS_CONTROL_LIST, AccessLevel.READ, user)
    return get_lookup(lookup_id).dict()
