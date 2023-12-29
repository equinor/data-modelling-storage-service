import json
from pathlib import Path

from storage.repository_interface import RepositoryInterface


class LocalFileRepository(RepositoryInterface):
    def __init__(self, location: str | Path | None = None):
        if location is None:
            location = f"{Path(__file__).parent.parent.parent}/SIMOS"
        self.path = Path(location)

    def get(self, absolute_ref: str) -> dict:
        try:
            path_to_json = absolute_ref.replace("dmss://system/SIMOS/", "")
            with open(f"{self.path}/{path_to_json}.json") as f:
                return json.load(f)
        except FileNotFoundError as ex:
            raise FileNotFoundError(
                f"'{absolute_ref}' not found. Are DMSS core blueprints available at '{self.path}'?"
            ) from ex
        except ValueError as ex:
            raise ValueError(f"Got invalid path for local repository blueprint path: '{absolute_ref}'") from ex

    def find(self, filter: dict, single=None, raw=None) -> dict:
        return self.get(filter["type"])

    def find_one(self, filters: dict) -> dict:
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
