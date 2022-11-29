from authentication.access_control import DEFAULT_ACL, access_control
from authentication.models import AccessLevel, User
from domain_classes.lookup import Lookup
from storage.internal.lookup_tables import insert_lookup


def create_lookup_table_use_case(name: str, table: Lookup, user: User) -> None:
    access_control(DEFAULT_ACL, AccessLevel.WRITE, user)
    insert_lookup(name, table.dict())
