import json
from pathlib import Path
from typing import Dict, Optional, Union

from storage.repository_interface import RepositoryInterface


class LocalFileRepository(RepositoryInterface):
    def __init__(self, location: Optional[Union[str, Path]] = None):
        if location is None:
            location = f"{str(Path(__file__).parent.parent.parent)}/home/"
        self.path = Path(location)

    def get(self, absolute_ref: str) -> dict:
        protocol, address = absolute_ref.split("://", 1)
        try:
            with open(f"{self.path}/{address}.json") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"'{absolute_ref}' not found. Are DMSS core blueprints available at '{self.path}'?"
            )

    def find(self, filter: dict, single=None, raw=None) -> dict:
        return self.get(filter["type"])

    def find_one(self, filters: Dict) -> Dict:
        raise NotImplementedError

    def add(self, document: dict) -> None:
        raise NotImplementedError

    def delete(self, document: dict) -> None:
        raise NotImplementedError

    def update(self, document: dict) -> None:
        raise NotImplementedError

    def get_blob(self, uid):
        raise NotImplementedError

    def delete_blob(self, uid: str):
        raise NotImplementedError

    def update_blob(self, uid: str, blob: bytearray):
        raise NotImplementedError
