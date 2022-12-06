import os
import tempfile
import zipfile

from authentication.models import User
from common.exceptions import ApplicationException
from domain_classes.tree_node import Node
from enums import SIMOS
from services.document_service import DocumentService
from storage.repositories.zip import ZipFileClient


def create_zip_export(document_service: DocumentService, absolute_document_ref: str, user: User) -> str:
    """Create a temporary folder on the host that contains a zip file with."""
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
    elif document_node.entity["type"] == SIMOS.PACKAGE.value and not document_node.entity["isRoot"]:
        # TODO handle non root pacakge
        raise ApplicationException(message="Create zip export is only supported for a single document (not a package)")
        # TODO add package.json file when exporting
    else:
        with zipfile.ZipFile(archive_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=5) as zip_file:
            # Save the selected node, using custom ZipFile repository
            document_service.save(document_node, data_source_id, ZipFileClient(zip_file), update_uncontained=True)
        return archive_path


def export_use_case(user: User, document_reference: str):
    memory_file = create_zip_export(
        document_service=DocumentService(user=user), absolute_document_ref=document_reference, user=user
    )
    return memory_file
