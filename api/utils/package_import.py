import json
import os
from typing import Dict, List, Union

from api.classes.dto import DTO
from api.config import Config
from api.core.enums import DMT
from api.core.repository.file import TemplateRepositoryFromFile
from api.core.repository.repository_exceptions import InvalidDocumentNameException
from api.core.utility import url_safe_name
from api.services.database import dmt_database as dmt_db
from api.utils.helper_functions import schemas_location
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


def _add_documents(path, documents, collection, is_entity=False) -> List[Dict]:
    docs = []
    for file in documents:
        logger.info(f"Working on {file}...")
        with open(f"{path}/{file}") as json_file:
            data = json.load(json_file)
        document = DTO(data)
        if not url_safe_name(document.name):
            raise InvalidDocumentNameException(document.name)
        dmt_db[collection].replace_one({"_id": document.uid}, document.data, upsert=True)
        docs.append({"_id": document.uid, "name": document.name, "type": document.type})
    return docs


def import_package(path, collection: str, is_root: bool = False, is_entity=False) -> Union[Dict]:
    # TODO: Package class
    package = {"name": os.path.basename(path), "type": DMT.PACKAGE.value, "isRoot": is_root}
    files = []
    directories = []
    for (path, directory, file) in os.walk(path):
        directories.extend(directory)
        files.extend(file)
        break

    package["content"] = _add_documents(path, documents=files, collection=collection, is_entity=is_entity)
    for folder in directories:
        package["content"].append(import_package(f"{path}/{folder}", is_root=False, collection=collection))

    package = DTO(package)
    dmt_db[collection].replace_one({"_id": package.uid}, package.data, upsert=True)
    logger.info(f"Imported package {package.name}")
    return {"_id": package.uid, "name": package.name, "type": package.type}
