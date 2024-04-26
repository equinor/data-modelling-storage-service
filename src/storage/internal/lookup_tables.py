from functools import lru_cache

from common.exceptions import NotFoundException
from config import config
from domain_classes.lookup import Lookup
from services.database import lookup_table_db


def insert_lookup(lookup_id: str, lookup: dict) -> None:
    lookup["_id"] = lookup_id
    lookup_table_db.set(lookup_id, lookup)


@lru_cache(maxsize=config.CACHE_MAX_SIZE)
def get_lookup(lookup_id: str) -> Lookup:
    lookup = lookup_table_db.get(lookup_id)
    if not lookup:
        raise NotFoundException(f"No lookup table with name '{lookup_id}' exists.")
    return Lookup(**lookup)


def delete_lookup(lookup_id: str) -> None:
    lookup_table_db.delete(lookup_id)
