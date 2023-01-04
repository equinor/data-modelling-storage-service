import json
from pathlib import Path
from zipfile import ZipFile

from common.utils.logging import logger
from common.utils.replace_reference_with_alias import (
    replace_absolute_references_in_entity_with_alias,
)
from domain_classes.dependency import Dependency
from enums import SIMOS
from storage.repository_interface import RepositoryInterface


class ZipFileClient(RepositoryInterface):
    def __init__(self, zip_file: ZipFile):
        self.zip_file = zip_file

    def update(self, entity: dict, storage_recipe=None, **kwargs):
        """
        Saves entity to zip file.

        By default, absolute references are resolved to aliases using the dependencies from entity["__combined_document_meta__"].
        """
        entity.pop("_id", None)
        entity.pop("uid", None)
        entity["__path__"] = entity["__path__"].rstrip("/")
        write_to = f"{entity['__path__']}/{entity['name']}.json"
        entity.pop("__path__")
        combined_document_meta = entity.pop("__combined_document_meta__")
        logger.debug(f"Writing: {entity['type']} to {write_to}")
        if entity["type"] != SIMOS.PACKAGE.value:
            if combined_document_meta:
                dependencies: list[Dependency] = [
                    Dependency(**dependency_dict) for dependency_dict in combined_document_meta["dependencies"]
                ]
                entity = replace_absolute_references_in_entity_with_alias(entity, dependencies)
            json_data = json.dumps(entity)
            binary_data = json_data.encode()
            self.zip_file.writestr(write_to, binary_data)
        elif "_meta_" in entity:
            self.zip_file.writestr(f"{Path(write_to).parent}/package.json", json.dumps(entity["_meta_"]).encode())

    def get(self, uid: str):
        return "Not implemented on ZipFile repository!"

    def add(self, uid: str, document: dict):
        return "Not implemented on ZipFile repository!"

    def delete(self, uid: str):
        return "Not implemented on ZipFile repository!"

    def find(self, filters):
        return "Not implemented on ZipFile repository!"

    def find_one(self, filters):
        return "Not implemented on ZipFile repository!"

    def delete_blob(self, uid: str):
        raise NotImplementedError

    def get_blob(self, uid: str) -> bytearray:
        raise NotImplementedError

    def update_blob(self, uid: str, blob: bytearray):
        raise NotImplementedError
