from authentication.access_control import DEFAULT_ACL, access_control
from authentication.models import AccessLevel, User
from storage.internal.lookup_tables import get_lookup


def get_lookup_table_use_case(lookup_id: str, user: User) -> dict:
    access_control(DEFAULT_ACL, AccessLevel.READ, user)
    return get_lookup(lookup_id).dict()
