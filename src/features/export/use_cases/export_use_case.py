import os
import tempfile
import zipfile

from authentication.models import User
from common.address import Address
from common.providers.address_resolver.address_resolver import (
    ResolvedAddress,
    resolve_address,
)
from common.tree.tree_node import Node
from enums import SIMOS
from features.export.use_cases.export_meta_use_case import export_meta_use_case
from services.document_service.document_service import DocumentService
from storage.repositories.zip.zip_file_client import ZipFileClient


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
        path = ""  # Path here is used to get the proper file structure in the zip file
        for node in document_node.traverse():
            if not node.storage_contained and not node.is_array():
                path = f"{path}/{node.entity.get('name', 'noname')}/" if path else node.entity.get("name", "noname")
                document_service.save(
                    node=node,
                    data_source_id=data_source_id,
                    path=path,
                    repository=storage_client,
                    combined_document_meta=document_meta,
                )


def create_zip_export(document_service: DocumentService, address: Address, user: User) -> str:
    """Create a temporary folder on the host that contains a zip file."""
    tmpdir = tempfile.mkdtemp()
    archive_path = os.path.join(tmpdir, "temp_zip_archive.zip")
    resolved_address: ResolvedAddress = resolve_address(address, document_service.get_data_source)
    document_node: Node = document_service.get_document(address, depth=999)

    # non-root packages and single documents will inherit the meta information from all parents.
    document_meta = {}
    if not (document_node.entity["type"] == SIMOS.PACKAGE.value and document_node.entity["isRoot"]):
        document_meta = export_meta_use_case(user=user, path_address=str(address))
    elif "_meta_" in document_node.entity:
        document_meta = document_node.entity["_meta_"]

    # TODO fix bug: relative references are resloved (if type is CarPackage/Wheel for an entity, the exported type is "dmss://DemoApplicationDataSource/models/CarPackage/Wheel"
    save_node_to_zipfile(
        archive_path=archive_path,
        document_service=document_service,
        document_node=document_node,
        document_meta=document_meta,
        data_source_id=resolved_address.data_source_id,
    )

    return archive_path


def export_use_case(user: User, address: str):
    memory_file = create_zip_export(
        document_service=DocumentService(user=user), address=Address.from_absolute(address), user=user
    )
    return memory_file
