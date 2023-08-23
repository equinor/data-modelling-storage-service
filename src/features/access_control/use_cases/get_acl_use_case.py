from authentication.models import AccessControlList
from domain_classes.document_look_up import DocumentLookUp
from storage.data_source_class import DataSource
from storage.internal.data_source_repository import DataSourceRepository


def get_acl_use_case(
    document_id: str, data_source_id: str, data_source_repository: DataSourceRepository
) -> AccessControlList:
    data_source: DataSource = data_source_repository.get(data_source_id)
    if document_id.startswith("$"):
        document_id = document_id[1:]
    lookup: DocumentLookUp = data_source.get_lookup(document_id)
    return lookup.acl
