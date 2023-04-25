from typing import Union

from enums import REFERENCE_TYPES, SIMOS
from storage.data_source_class import DataSource


def delete_list_recursive(value: Union[list, dict], data_source: DataSource):
    """
    Digs down in any list (simple, matrix, complex), and delete any contained referenced documents
    """
    if isinstance(value, list):
        [delete_list_recursive(item, data_source) for item in value]
    elif isinstance(value, dict):
        delete_dict_recursive(value, data_source)


def delete_dict_recursive(in_dict: dict, data_source: DataSource):
    if (
        in_dict.get("type") == SIMOS.REFERENCE.value and in_dict.get("referenceType") == REFERENCE_TYPES.STORAGE.value
    ):  # It's a model contained reference
        delete_document(data_source, in_dict["address"])
    elif in_dict.get("type") == SIMOS.BLOB.value:
        data_source.delete_blob(in_dict["_blob_id"])
    else:
        for value in in_dict.values():
            if isinstance(value, dict) or isinstance(value, list):  # Potentially complex
                if not value:
                    continue
                if isinstance(value, list):
                    delete_list_recursive(value, data_source)
                else:
                    delete_dict_recursive(value, data_source)


def delete_document(data_source: DataSource, document_id: str):
    """
    Delete a document, and any model contained children.
    """
    document: dict = data_source.get(document_id)
    delete_dict_recursive(document, data_source)
    data_source.delete(document_id)
