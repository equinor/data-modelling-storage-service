import unittest
from unittest import mock

from authentication.models import User
from common.tree.tree_node import Node
from common.tree.tree_node_serializer import tree_node_from_dict
from config import config
from enums import StorageDataTypes
from storage.data_source_class import DataSource
from tests.unit.mocks.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mocks.mock_document_service import get_mock_document_service
from tests.unit.mocks.mock_recipe_provider import MockStorageRecipeProvider

config.AUTH_ENABLED = False
test_user = User(**{"user_id": "unit-test", "full_name": "Unit Test", "email": "unit-test@example.com"})


class DataSourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        simos_blueprints = ["dmss://system/SIMOS/Entity", "dmss://system/SIMOS/NamedEntity"]
        mock_blueprint_folder = "src/tests/unit/services/document_service/mock_blueprints/blob_blueprints"
        mock_blueprints_and_file_names = {
            "blobContainer": "blobContainer.blueprint.json",
            "blob": "blob.blueprint.json",
            "uncontained_blueprint": "uncontained_blueprint.blueprint.json",
        }
        mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        )
        mock_recipe_folder = (
            "src/tests/unit/services/document_service/mock_blueprints/blob_blueprints/mock_storage_recipes.json"
        )
        self.recipe_provider = MockStorageRecipeProvider(mock_recipe_folder).provider
        self.mock_document_service = get_mock_document_service(blueprint_provider=mock_blueprint_provider)

    def test_save_into_multiple_repositories(self):
        uncontained_doc = {
            "name": "Parent",
            "description": "",
            "type": "uncontained_blueprint",
            "uncontained_in_every_way": {
                "name": "a_reference",
                "type": "dmss://system/SIMOS/NamedEntity",
                "_id": "$2",
            },
        }

        default_doc_storage: dict = {}

        def default_get(document_id: str):
            return default_doc_storage[document_id]

        def default_update(uid, data):
            default_doc_storage[uid] = data
            return None

        blob_doc_storage: dict = {}

        def blob_get(document_id: str):
            return blob_doc_storage[document_id]

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

        self.mock_document_service.repository_provider = lambda x, y: data_source
        self.mock_document_service.user = test_user

        node: Node = tree_node_from_dict(
            uncontained_doc,
            uid="1",
            blueprint_provider=self.mock_document_service.get_blueprint,
            recipe_provider=self.recipe_provider,
        )

        for sub_node in node.traverse():
            if not sub_node.storage_contained and not sub_node.is_array():
                self.mock_document_service.save(node=sub_node, data_source_id="testing")

        # Test that both repos gets written into
        assert blob_doc_storage and default_doc_storage

    def test_save_based_on_root_storageRecipe(self):
        blob_doc = {
            "name": "some_entity",
            "description": "",
            "type": "blob",
            "someData": "test",
        }

        default_doc_storage: dict = {}

        def default_get(document_id: str):
            return default_doc_storage[document_id]

        def default_update(uid, data):
            default_doc_storage[uid] = data
            return None

        blob_doc_storage: dict = {}

        def blob_get(document_id: str):
            return blob_doc_storage[document_id]

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

        self.mock_document_service.repository_provider = lambda x, y: data_source
        self.mock_document_service.user = test_user

        node: Node = tree_node_from_dict(
            blob_doc,
            uid="1",
            blueprint_provider=self.mock_document_service.get_blueprint,
            recipe_provider=self.recipe_provider,
        )

        self.mock_document_service.save(node, "testing")

        # Test that only the blob storage is written into
        assert blob_doc_storage and not default_doc_storage

    def test_save_nested_based_on_root_storageRecipe(self):
        blob_doc = {
            "name": "some_entity",
            "description": "",
            "type": "blobContainer",
            "blob": {
                "name": "test",
                "type": "blob",
                "description": "",
                "someData": "Hallo World!",
            },
        }

        default_doc_storage: dict = {}

        def default_get(document_id: str):
            return default_doc_storage[document_id]

        def default_update(uid, data):
            default_doc_storage[uid] = data
            return None

        blob_doc_storage: dict = {}

        def blob_get(document_id: str):
            return blob_doc_storage[document_id]

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
        self.mock_document_service.repository_provider = lambda x, y: data_source
        self.mock_document_service.user = test_user

        node: Node = tree_node_from_dict(
            blob_doc,
            self.mock_document_service.get_blueprint,
            uid="1",
            recipe_provider=self.recipe_provider,
        )

        for sub_node in node.traverse():
            if not sub_node.storage_contained and not sub_node.is_array():
                self.mock_document_service.save(node=sub_node, data_source_id="testing")

        # Test that both repos gets written into
        assert blob_doc_storage and default_doc_storage
