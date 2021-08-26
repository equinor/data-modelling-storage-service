from typing import Union

from domain_classes.dto import DTO
from storage.data_source_class import DataSource


def delete_complex_list(value: Union[list, dict], data_source: DataSource):
    """
    Digs down in any list (simple, matrix, complex), and delete any contained referenced documents
    """
    if isinstance(value, list):
        [delete_complex_list(item, data_source) for item in value]

    # No more nested lists
    if not isinstance(value, dict):  # References are dicts
        return

    if value.get("_id") and value.get("contained"):  # If the referenced document is model contained, delete it.
        delete_document(data_source, value["_id"])


def delete_document(data_source: DataSource, document_id: str):
    """
    Delete a document, and any model contained children.
    """
    document: DTO = data_source.get(document_id)
    # Delete model contained referenced documents, and then itself
    for key, value in document.data.items():
        if isinstance(value, dict) or isinstance(value, list):  # Potentially complex
            if not value:
                continue
            if isinstance(value, list):
                delete_complex_list(value, data_source)
            else:
                value: dict
                if value.get("_id") and value.get("contained") is True:  # It's a model contained reference
                    delete_document(data_source, value["_id"])
    data_source.delete(document_id)
