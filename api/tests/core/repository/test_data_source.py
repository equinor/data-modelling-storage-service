import unittest
from unittest import mock

from api.classes.dto import DTO
from api.classes.tree_node import Node
from api.core.enums import StorageDataTypes
from api.core.service.document_service import DocumentService
from api.core.storage.data_source import DataSource
from api.tests.core.document_service.common import blueprint_provider


class DataSourceTestCase(unittest.TestCase):
    def test_save_into_multiple_repositories(self):
        uncontained_doc = {
            "name": "Parent",
            "description": "",
            "type": "uncontained_blueprint",
            "uncontained_in_every_way": {"name": "a_reference", "type": "blueprint_2"},
        }

        default_doc_storage = {}

        def default_get(document_id: str):
            return DTO(default_doc_storage[document_id])

        def default_update(uid, data):
            default_doc_storage[uid] = data
            return None

        blob_doc_storage = {}

        def blob_get(document_id: str):
            return DTO(blob_doc_storage[document_id])

        def blob_update(uid, data):
            blob_doc_storage[uid] = data
            return None

        default_repo = mock.Mock()
        default_repo.data_types = [StorageDataTypes.DEFAULT]
        default_repo.get = default_get
        default_repo.update = default_update

        blob_repo = mock.Mock()
        blob_repo.data_types = [StorageDataTypes.BLOB]
        blob_repo.get = blob_get
        blob_repo.update = blob_update

        data_source_collection = mock.Mock()

        def mock_find_one(**kwargs):
            return None

        data_source_collection.find_one = mock_find_one

        data_source = DataSource(
            name="testing",
            repositories={"default": default_repo, "blob": blob_repo},
            data_source_collection=data_source_collection,
        )

        def repository_provider(data_source_id):
            if data_source_id == "testing":
                return data_source

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=repository_provider
        )

        node: Node = Node.from_dict(uncontained_doc, "1", blueprint_provider)

        document_service.save(node, "testing")

        # Test that both repos get's written into
        assert blob_doc_storage and default_doc_storage
