import unittest
from unittest import mock

from authentication.models import User
from domain_classes.dto import DTO
from domain_classes.tree_node import Node
from enums import StorageDataTypes
from services.document_service import DocumentService
from storage.data_source_class import DataSource
from tests.unit.mock_blueprint_provider import blueprint_provider
from config import config

config.AUTH_ENABLED = False
test_user = User(**{"username": "unit-test", "full_name": "Unit Test", "email": "unit-test@example.com"})


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
        default_repo.name = "default"
        default_repo.data_types = [StorageDataTypes.DEFAULT]
        default_repo.get = default_get
        default_repo.update = default_update

        blob_repo = mock.Mock()
        blob_repo.name = "blob"
        blob_repo.data_types = [StorageDataTypes.BLOB]
        blob_repo.get = blob_get
        blob_repo.update = blob_update

        data_source_collection = mock.Mock()

        def mock_find_one(**kwargs):
            return None

        data_source_collection.find_one = mock_find_one

        data_source = DataSource(
            name="testing",
            user=test_user,
            repositories={"default": default_repo, "blob": blob_repo},
            data_source_collection=data_source_collection,
        )

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x, y: data_source, user=test_user
        )

        node: Node = Node.from_dict(uncontained_doc, "1", document_service.get_blueprint)

        document_service.save(node, "testing", update_uncontained=True)

        # Test that both repos get's written into
        assert blob_doc_storage and default_doc_storage

    def test_save_based_on_root_storageRecipe(self):
        blob_doc = {"name": "some_entity", "description": "", "type": "blob", "someData": ""}

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
        default_repo.name = "default"
        default_repo.data_types = [StorageDataTypes.DEFAULT]
        default_repo.get = default_get
        default_repo.update = default_update

        blob_repo = mock.Mock()
        blob_repo.name = "blob"
        blob_repo.data_types = [StorageDataTypes.BLOB]
        blob_repo.get = blob_get
        blob_repo.update = blob_update

        data_source_collection = mock.Mock()

        def mock_find_one(**kwargs):
            return None

        data_source_collection.find_one = mock_find_one

        data_source = DataSource(
            name="testing",
            user=test_user,
            repositories={"default": default_repo, "blob": blob_repo},
            data_source_collection=data_source_collection,
        )

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x, y: data_source, user=test_user
        )

        node: Node = Node.from_dict(blob_doc, "1", document_service.get_blueprint)

        document_service.save(node, "testing")

        # Test that only the blob storage is written into
        assert blob_doc_storage and not default_doc_storage

    def test_save_nested_based_on_root_storageRecipe(self):
        blob_doc = {
            "name": "some_entity",
            "description": "",
            "type": "blobContainer",
            "blob": {"name": "test", "type": "blob", "description": "", "someData": "Hallo World!"},
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
        default_repo.name = "default"
        default_repo.data_types = [StorageDataTypes.DEFAULT]
        default_repo.get = default_get
        default_repo.update = default_update

        blob_repo = mock.Mock()
        blob_repo.name = "blob"
        blob_repo.data_types = [StorageDataTypes.BLOB]
        blob_repo.get = blob_get
        blob_repo.update = blob_update

        data_source_collection = mock.Mock()

        def mock_find_one(**kwargs):
            return None

        data_source_collection.find_one = mock_find_one

        data_source = DataSource(
            name="testing",
            user=test_user,
            repositories={"default": default_repo, "blob": blob_repo},
            data_source_collection=data_source_collection,
        )

        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x, y: data_source, user=test_user
        )

        node: Node = Node.from_dict(blob_doc, "1", document_service.get_blueprint)

        document_service.save(node, "testing", update_uncontained=True)

        # Test that both repos get's written into
        assert blob_doc_storage and default_doc_storage
