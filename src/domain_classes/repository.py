import importlib
import traceback
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path

from common.exceptions import ApplicationException
from config import config
from domain_classes.blueprint import Blueprint
from enums import StorageDataTypes
from storage.repositories.azure_blob import AzureBlobStorageClient
from storage.repositories.mongo import MongoDBClient
from storage.repositories.sql import SQLRepository
from storage.repository_interface import RepositoryInterface


class Repository(RepositoryInterface):
    def __init__(self, name, get_blueprint: Callable[[str], Blueprint], data_types: list[str] | None = None, **kwargs):
        self.name = name
        self.data_types = [StorageDataTypes(d) for d in data_types] if data_types else []
        self.client = self._get_client(get_blueprint, **kwargs)

    def update(self, uid: str, document: dict) -> bool:
        return self.client.update(uid, document)

    def get(self, uid: str) -> dict:
        return self.client.get(uid)

    def delete(self, uid: str) -> bool:
        return self.client.delete(uid)

    def delete_blob(self, uid: str) -> bool:
        return self.client.delete_blob(uid)

    def find(self, filters: dict) -> list[dict] | None:
        return self.client.find(filters)

    def find_one(self, filters: dict) -> dict:
        return self.client.find_one(filters)

    def add(self, uid: str, document: dict) -> bool:
        return self.client.add(uid, document)

    def update_blob(self, uid: str, blob: bytes) -> bool:
        return self.client.update_blob(uid, blob)

    def get_blob(self, uid: str) -> bytes:
        return self.client.get_blob(uid)

    @staticmethod
    @lru_cache(maxsize=config.CACHE_MAX_SIZE)
    def _get_client(get_blueprint, **kwargs):
        if kwargs["type"] == "mongo-db":
            return MongoDBClient(**kwargs, get_blueprint=get_blueprint)

        if kwargs["type"] == "sql":
            return SQLRepository(**kwargs, get_blueprint=get_blueprint)

        if kwargs["type"] == "azure_blob":
            return AzureBlobStorageClient(**kwargs, get_blueprint=get_blueprint)

        else:
            """Get the repository client from a plugin.

            Repository plugins must be placed in the "storage/repository_plugins" directory.
            Each plugin must have a folder with at least one file: __init__.py
            This __init__ file must implement a class called "Repository" that inherits from the Repository class.

            If the plugin requires any pypi-packages, add a "requirements.txt"-file generated by "pip freeze" in the
            plugins root folder.

            To use this repository plugin, create a repository in a data source definition, with the type matching
            the plugin name (name of the folder)
            """

            repository_plugins_dir_path = Path(__file__).parent.parent / "storage" / "repository_plugins"
            repository_plugins_dirs = []

            for file in repository_plugins_dir_path.iterdir():
                if file.is_dir() and file.name[0] != "_":  # Python modules can not start with "_"
                    repository_plugins_dirs.append(str(file).replace("/code/src/", "").replace("/", "."))

                try:
                    modules = [importlib.import_module(module) for module in repository_plugins_dirs]
                    for repository_plugin in modules:
                        if kwargs["type"] == repository_plugin.__name__.split(".")[-1]:
                            return repository_plugin.Repository(
                                get_blueprint=get_blueprint,
                                **kwargs,
                            )
                except ImportError as error:
                    traceback.print_exc()
                    raise ImportError(
                        f"Failed to import a repository plugin module: '{error}'"
                        + "Make sure the module has a '_init_.py' file, and a 'Repository' class implementing "
                        + "the RepositoryInterface"
                    ) from error

            raise ApplicationException(f"No repository plugin type '{kwargs['type']}' is configured")
