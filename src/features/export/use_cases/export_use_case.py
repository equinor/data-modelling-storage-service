import os
import tempfile
import zipfile

from authentication.models import User
from common.exceptions import ApplicationException
from domain_classes.tree_node import Node
from enums import SIMOS
from services.document_service import DocumentService
from storage.repositories.zip import ZipFileClient
from features.export.use_cases.export_meta_use_case import _collect_entity_meta_by_path

def create_zip_export(document_service: DocumentService, absolute_document_ref: str, user: User) -> str:
    """Create a temporary folder on the host that contains a zip file.s"""
    tmpdir = tempfile.mkdtemp()
    archive_path = os.path.join(tmpdir, "temp_zip_archive.zip")

    data_source_id, document_path = absolute_document_ref.split("/", 1)
    document_node: Node = document_service.get_by_path(absolute_document_ref)
    if document_node.entity["type"] == SIMOS.PACKAGE.value and document_node.entity["isRoot"]:
        with zipfile.ZipFile(archive_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=5) as zip_file:
            # Save the selected node, using custom ZipFile repository
            storage_client = ZipFileClient(zip_file)
            document_service.save(document_node, data_source_id, storage_client, update_uncontained=True)

        return archive_path
    if document_node.entity["type"] == SIMOS.PACKAGE.value and not document_node.entity["isRoot"]:
        raise ApplicationException(
            message="Create zip export is only supported for a single document and root package"
        )

    # with zipfile.ZipFile(archive_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=5) as zip_file:
    #     # when exporting a single file, the exported file will inherit meta attribute from its parent
    #     parent_path = document_path.rsplit("/", 1)[0]
    #     parent_node: Node = document_service.get_by_path(f"{data_source_id}/{parent_path}")
    #     if "_meta_" in parent_node.entity:
    #         document_node.entity["_meta_"] = parent_node.entity["_meta_"] #TODO override is not correct. use _collect_entity_meta_by_path
    #         # ????
    #     document_service.save(document_node, data_source_id, ZipFileClient(zip_file), update_uncontained=True)
    return archive_path


def export_use_case(user: User, document_reference: str):
    memory_file = create_zip_export(
        document_service=DocumentService(user=user), absolute_document_ref=document_reference, user=user
    )
    return memory_file
