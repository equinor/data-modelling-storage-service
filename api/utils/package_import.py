import json
import os
from typing import Dict, List, Union

from api.classes.dto import DTO
from api.core.enums import DMT
from api.core.storage.data_source import DataSource
from api.core.storage.repository_exceptions import InvalidDocumentNameException
from api.core.storage.internal.data_source_repository import get_data_source
from api.core.utility import url_safe_name
from api.utils.logging import logger


def get_template_type(directory: str, file: str) -> str:
    path = f"{directory}/{file}"
    if path.endswith(".json"):
        path = path[: -len(".json")]
    if "/core/" in path:
        path = replace_prefix(path, "system", "core")
    elif "/blueprints/" in path:
        path = replace_prefix(path, "SSR-DataSource", "blueprints")
    else:
        raise ValueError
    return path


def replace_prefix(path, prefix, where):
    index = path.find(f"/{where}/")
    return f"{prefix}/{path[index + len(f'/{where}/'):]}"


def _add_documents(path, documents, data_source) -> List[Dict]:
    docs = []
    for file in documents:
        logger.info(f"Working on {file}...")
        with open(f"{path}/{file}") as json_file:
            data = json.load(json_file)
        document = DTO(data)
        if not url_safe_name(document.name):
            raise InvalidDocumentNameException(document.name)
        data_source.add(document)
        docs.append({"_id": document.uid, "name": document.name, "type": document.type})

    return docs


def import_package(path, data_source: str, is_root: bool = False) -> Union[Dict]:
    data_source: DataSource = get_data_source(data_source_id=data_source)
    package = {"name": os.path.basename(path), "type": DMT.PACKAGE.value, "isRoot": is_root}
    files = []
    directories = []

    for (path, directory, file) in os.walk(path):
        directories.extend(directory)
        files.extend(file)
        break

    package["content"] = _add_documents(path, files, data_source)
    for folder in directories:
        package["content"].append(import_package(f"{path}/{folder}", is_root=False, data_source=data_source.name))

    package = DTO(package)
    data_source.add(package)
    logger.info(f"Imported package {package.name}")
    return {"_id": package.uid, "name": package.name, "type": package.type}
