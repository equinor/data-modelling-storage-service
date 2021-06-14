import json
import os
from typing import Dict, List, Union

from domain_classes.dto import DTO
from enums import DMT
from storage.data_source_class import DataSource
from storage.internal.data_source_repository import get_data_source
from utils.exceptions import EntityAlreadyExistsException, InvalidDocumentNameException, RootPackageNotFoundException
from utils.find_document_by_path import get_document_by_ref
from utils.logging import logger
from utils.string_helpers import url_safe_name


def _add_documents(path, documents, data_source) -> List[Dict]:
    docs = []
    for file in documents:
        logger.debug(f"Working on {file}...")
        with open(f"{path}/{file}") as json_file:
            data = json.load(json_file)
        document = DTO(data)
        if not url_safe_name(document.name):
            raise InvalidDocumentNameException(document.name)
        # TODO: How to deal with nodes storage_attribute here?
        data_source.add(document)
        docs.append({"_id": document.uid, "name": document.name, "type": document.type})

    return docs


def import_package(path, data_source: str, is_root: bool = False) -> Union[Dict]:
    data_source: DataSource = get_data_source(data_source_id=data_source)
    package = {"name": os.path.basename(path), "type": DMT.PACKAGE.value, "isRoot": is_root}
    try:
        if get_document_by_ref(f"{data_source.name}/{package['name']}"):
            raise EntityAlreadyExistsException(
                message=(
                    f"A root package with name '{package['name']}' "
                    "already exists in data source '{data_source.name}'"
                )
            )
    except RootPackageNotFoundException:
        pass

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
