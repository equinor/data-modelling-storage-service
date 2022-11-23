import os
import tempfile
import zipfile

from authentication.models import User
from domain_classes.tree_node import Node
from services.document_service import DocumentService
from storage.repositories.zip import ZipFileClient


def create_zip_export(document_service: DocumentService, absolute_document_ref: str) -> str:
    """Create a temproary folder on the host that contains a zip file with."""
    tmpdir = tempfile.mkdtemp()
    archive_path = os.path.join(tmpdir, "temp_zip_archive.zip")

    data_source_id, document_path = absolute_document_ref.split("/", 1)
    document: Node = document_service.get_by_path(absolute_document_ref)
    # TODO add meta information to the document. Single document,
    # root package and non root packages needs to be handled in different ways
    with zipfile.ZipFile(archive_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=5) as zip_file:
        # Save the selected node, using custom ZipFile repository
        document_service.save(document, data_source_id, ZipFileClient(zip_file), update_uncontained=True)
    return archive_path


def export_use_case(user: User, document_reference: str):
    memory_file = create_zip_export(
        document_service=DocumentService(user=user), absolute_document_ref=document_reference
    )
    return memory_file
