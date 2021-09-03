from typing import Union

from domain_classes.dto import DTO
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
    in_dict: dict
    if in_dict.get("_id") and in_dict.get("contained") is True:  # It's a model contained reference
        delete_document(data_source, in_dict["_id"])
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
    document: DTO = data_source.get(document_id)
    delete_dict_recursive(document.data, data_source)
    data_source.delete(document_id)
