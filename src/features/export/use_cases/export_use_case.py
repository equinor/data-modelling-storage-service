import os
import tempfile
import zipfile

from authentication.models import User
from domain_classes.tree_node import Node
from enums import SIMOS
from features.export.use_cases.export_meta_use_case import export_meta_use_case
from services.document_service import DocumentService
from storage.repositories.zip import ZipFileClient


def save_node_to_zipfile(
    archive_path: str,
    document_node: Node,
    document_service: DocumentService,
    data_source_id: str,
    document_meta: dict | None,
):
    with zipfile.ZipFile(archive_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=5) as zip_file:
        if document_meta:
            document_node.entity["_meta_"] = document_meta
        storage_client = ZipFileClient(zip_file)
        document_service.save(
            document_node,
            data_source_id,
            storage_client,
            combined_document_meta=document_meta,
        )


def create_zip_export(document_service: DocumentService, absolute_document_ref: str, user: User) -> str:
    """Create a temporary folder on the host that contains a zip file."""
    tmpdir = tempfile.mkdtemp()
    archive_path = os.path.join(tmpdir, "temp_zip_archive.zip")

    data_source_id, document_path = absolute_document_ref.split("/", 1)
    document_node: Node = document_service.get_document(f"/{absolute_document_ref}")

    # non-root packages and single documents will inherit the meta information from all parents.
    document_meta = {}
    if not (document_node.entity["type"] == SIMOS.PACKAGE.value and document_node.entity["isRoot"]):
        document_meta = export_meta_use_case(user=user, document_reference=absolute_document_ref)
    elif "_meta_" in document_node.entity:
        document_meta = document_node.entity["_meta_"]

    # TODO fix bug: relative references are resloved (if type is CarPackage/Wheel for an entity, the exported type is "dmss://DemoApplicationDataSource/models/CarPackage/Wheel"
    save_node_to_zipfile(
        archive_path=archive_path,
        document_service=document_service,
        document_node=document_node,
        document_meta=document_meta,
        data_source_id=data_source_id,
    )

    return archive_path


def export_use_case(user: User, document_reference: str):
    memory_file = create_zip_export(
        document_service=DocumentService(user=user), absolute_document_ref=document_reference, user=user
    )
    return memory_file
