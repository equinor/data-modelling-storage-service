import json
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
        write_to = f"{entity['__path__']}/{entity['name']}.json"
        entity.pop("__path__")
        json_data = json.dumps(entity)
        binary_data = json_data.encode()
        logger.debug(f"Writing: {entity['type']} to {write_to}")
        if entity["type"] != SIMOS.PACKAGE.value:
            self.zip_file.writestr(write_to, binary_data)

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
