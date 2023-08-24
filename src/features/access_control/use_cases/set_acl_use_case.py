from authentication.models import AccessControlList
from common.address import Address
from common.exceptions import MissingPrivilegeException
from common.utils.logging import logger
from services.document_service import DocumentService
from storage.data_source_class import DataSource
from storage.internal.data_source_repository import DataSourceRepository


def set_acl_use_case(
    data_source_id: str,
    document_id: str,
    acl: AccessControlList,
    recursively: bool,
    data_source_repository: DataSourceRepository,
    document_service: DocumentService,
):
    if "." in document_id:
        raise Exception(
            f"set_acl() function got document_id: {document_id}. "
            f"The set_acl() function can only be used on root documents. You cannot use a dotted document id."
        )
    data_source: DataSource = data_source_repository.get(data_source_id)

    if not recursively:  # Only update acl on the one document
        data_source.update_access_control(document_id, acl)
        return

    # TODO: Updating ACL for Links should only be additive
    # TODO: ACL for StorageReferences should always be identical to parent document
    root_node = document_service.get_document(Address(document_id, data_source_id), 99)
    data_source.update_access_control(root_node.node_id, acl)
    for child in root_node.children:
        for node in child.traverse():
            if not node.storage_contained and not node.is_array():
                try:
                    data_source.update_access_control(node.entity["_id"], acl)
                except MissingPrivilegeException:  # The user might not have permission on a referenced document
                    logger.warning(f"Failed to update ACL on {node.node_id}. Permission denied.")
    return "OK"
