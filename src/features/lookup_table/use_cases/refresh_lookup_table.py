from authentication.access_control import AccessControlList, assert_user_has_access
from authentication.models import AccessLevel, User
from features.lookup_table.use_cases.create_lookup_table import create_lookup_table_use_case
from storage.internal.lookup_tables import get_lookup


def refresh_lookup_table_use_case(lookup_id: str, user: User) -> None:
    assert_user_has_access(AccessControlList.default(), AccessLevel.WRITE, user)
    paths = get_lookup(lookup_id).paths
    return create_lookup_table_use_case(paths, lookup_id, user)
