import json
from pathlib import Path
from zipfile import ZipFile

from common.utils.logging import logger
from enums import SIMOS
from storage.repository_interface import RepositoryInterface


class ZipFileClient(RepositoryInterface):
    def __init__(self, zip_file: ZipFile):
        self.zip_file = zip_file

    def update(self, entity: dict, storage_recipe=None, **kwargs):
        entity.pop("_id", None)
        entity.pop("uid", None)
        if "/" in entity["__path__"][-1]:
            entity["__path__"] = entity["__path__"][:-1]
        write_to = f"{entity['__path__']}/{entity['name']}.json"
        entity.pop("__path__")
        json_data = json.dumps(entity)
        binary_data = json_data.encode()
        logger.debug(f"Writing: {entity['type']} to {write_to}")
        if entity["type"] != SIMOS.PACKAGE.value:
            self.zip_file.writestr(write_to, binary_data)
        else:
            self.zip_file.writestr(f"{Path(write_to).parent}/package.json", json.dumps(entity["_meta_"]).encode())

    def get(self, uid: str):
        return "Not implemented on ZipFile repository!"

    def add(self, document: dict, path: str, filename: str = None):
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
