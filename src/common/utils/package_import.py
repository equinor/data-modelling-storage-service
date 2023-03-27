import json
import os
from typing import Dict, List, Union
from uuid import uuid4

from authentication.models import User
from common.exceptions import BadRequestException, NotFoundException
from common.utils.get_document_by_path import get_document_by_absolute_path
from common.utils.logging import logger
from common.utils.string_helpers import url_safe_name
from enums import SIMOS
from storage.data_source_class import DataSource
from storage.internal.data_source_repository import get_data_source


def _add_documents(path, documents, data_source) -> List[Dict]:
    docs = []
    for file in documents:
        logger.debug(f"Working on {file}...")
        with open(f"{path}/{file}") as json_file:
            document = json.load(json_file)
        if document.get("name") and not url_safe_name(document["name"]):
            raise BadRequestException(
                message=f"'{document['name']}' is a invalid document name. "
                f"Only alphanumeric, underscore, and dash are allowed characters"
            )
        document["_id"] = document.get("_id", str(uuid4()))
        data_source.update(document)
        docs.append(
            {
                "ref": document["_id"],
                "targetName": document.get("name"),
                "targetType": document["type"],
                "type": SIMOS.LINK.value,
            }
        )

    return docs


def import_package(path, user: User, data_source_name: str, is_root: bool = False) -> Union[Dict]:
    data_source: DataSource = get_data_source(data_source_id=data_source_name, user=user)
    package = {"name": os.path.basename(path), "type": SIMOS.PACKAGE.value, "isRoot": is_root}
    try:
        if get_document_by_absolute_path(f"dmss://{data_source.name}/{package['name']}", user):
            raise BadRequestException(
                message=(
                    f"A root package with name '{package['name']}' "
                    "already exists in data source '{data_source.name}'"
                )
            )
    except (NotFoundException, NotFoundException):
        pass

    files = []
    directories = []

    for path, directory, file in os.walk(path):
        directories.extend(directory)
        files.extend(file)
        break

    package["content"] = _add_documents(path, files, data_source)
    for folder in directories:
        package["content"].append(
            import_package(f"{path}/{folder}", user, is_root=False, data_source_name=data_source.name)
        )

    data_source.update(package)
    logger.info(f"Imported package {package['name']}")
    return {
        "ref": package["_id"],
        "targetType": package["type"],
        "targetName": package.get("name"),
        "type": SIMOS.LINK.value,
    }
