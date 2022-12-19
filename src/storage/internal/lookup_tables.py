from pymongo.errors import DuplicateKeyError

from common.exceptions import BadRequestException, NotFoundException
from domain_classes.lookup import Lookup
from services.database import lookup_table_collection


def insert_lookup(lookup_id: str, lookup: dict) -> None:
    lookup["_id"] = lookup_id
    try:
        lookup_table_collection.insert_one(lookup)
    except DuplicateKeyError:
        raise BadRequestException(
            f"A lookup table with name '{lookup['_id']}' already exists."
            + " Use a different name, or delete the old one first"
        )


def get_lookup(lookup_id: str) -> Lookup:
    lookup = lookup_table_collection.find_one(filter={"_id": lookup_id})
    if not lookup:
        raise NotFoundException(f"No lookup table with name '{lookup_id}' exists.")
    return Lookup(**lookup)


def delete_lookup(lookup_id: str) -> None:
    try:
        lookup_table_collection.remove(filter={"_id": lookup_id})
    except NotFoundException:  # TODO: replace with actual exception from pymongo
        pass
