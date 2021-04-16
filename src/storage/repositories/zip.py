import json
from zipfile import ZipFile

from domain_classes.dto import DTO
from enums import DMT
from storage.repository_interface import RepositoryInterface
from utils.logging import logger


class ZipFileClient(RepositoryInterface):
    def __init__(self, zip_file: ZipFile):
        self.zip_file = zip_file

    def update(self, dto: DTO, storage_recipe=None):
        dto.data.pop("_id", None)
        dto.data.pop("uid", None)
        json_data = json.dumps(dto.data)
        binary_data = json_data.encode()
        write_to = f"{dto.data['__path__']}/{dto.name}.json"
        logger.info(f"Writing: {dto.type} to {write_to}")

        if dto.type != DMT.PACKAGE.value:
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
