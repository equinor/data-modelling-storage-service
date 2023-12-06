from common.entity.find import find
from common.exceptions import NotFoundException
from common.utils.logging import logger
from enums import REFERENCE_TYPES, SIMOS, StorageDataTypes
from storage.data_source_class import DataSource


def _delete_list_recursive(value: list | dict, data_source: DataSource):
    """
    Digs down in any list (simple, matrix, complex), and delete any contained referenced documents
    """
    if isinstance(value, list):
        [_delete_list_recursive(item, data_source) for item in value]
    elif isinstance(value, dict):
        _delete_dict_recursive(value, data_source)


def delete_by_attribute_path(document: dict, path: list[str], data_source: DataSource) -> dict:
    path_elements = [e.strip("[]./") for e in path]
    # Step through all the path items except the last one that should be deleted
    target = find(document, path_elements[:-1])

    if isinstance(target, list):
        obj = target[int(path_elements[-1])]
        del target[int(path_elements[-1])]
    elif isinstance(target, dict):
        obj = target[path_elements[-1]]
        del target[path_elements[-1]]
    else:
        raise ValueError(f"Invalid path {path}.")

    if isinstance(obj, list):
        _delete_list_recursive(obj, data_source=data_source)
    if isinstance(obj, dict):
        _delete_dict_recursive(obj, data_source=data_source)

    return document


def _delete_dict_recursive(in_dict: dict, data_source: DataSource):
    if (
        in_dict.get("type") == SIMOS.REFERENCE.value and in_dict.get("referenceType") == REFERENCE_TYPES.STORAGE.value
    ):  # It's a model contained reference
        try:
            delete_document(data_source, in_dict["address"])
        except NotFoundException:  # storage address was empty so there is nothing to delete
            logger.warning(f"STOARGE ADDRESS {in_dict['address']} NOT FOUND: SKIPPING")

    elif in_dict.get("type") == SIMOS.BLOB.value:
        data_source.delete_blob(in_dict["_blob_id"])
    else:
        for value in in_dict.values():
            if isinstance(value, dict) or isinstance(value, list):  # Potentially complex
                if not value:
                    continue
                if isinstance(value, list):
                    _delete_list_recursive(value, data_source)
                else:
                    _delete_dict_recursive(value, data_source)


def delete_document(data_source: DataSource, document_id: str):
    """
    Delete a document, and any model contained children.
    """
    if document_id.startswith("$"):
        document_id = document_id[1:]
    if data_source.get_storage_affinity(document_id) == StorageDataTypes.BLOB:
        data_source.delete_blob(document_id)
    else:
        document: dict = data_source.get(document_id)
        _delete_dict_recursive(document, data_source)
        data_source.delete(document_id)
