import unittest
from unittest import mock

from authentication.models import User
from common.tree_node_serializer import tree_node_from_dict
from config import config
from domain_classes.tree_node import Node
from enums import StorageDataTypes
from storage.data_source_class import DataSource
from tests.unit.mock_utils import (
    get_mock_document_service,
    mock_storage_recipe_provider,
)
from enums import SIMOS
config.AUTH_ENABLED = False
test_user = User(**{"user_id": "unit-test", "full_name": "Unit Test", "email": "unit-test@example.com"})


class DataSourceTestCase(unittest.TestCase):
    def test_save_with_update_uncontained_false(self):
        basic_entity = {"_id": "2", "name": "exampleEntity", "description": "", "type": "basic_blueprint"}
        document = {
            "name": "Parent",
            "description": "",
            "type": "uncontained_blueprint",
            "uncontained_in_every_way": basic_entity # according to blueprint, uncontained_in_every_way is model uncontained.
        }
        # TODO move default_doc_storage, default_get, default_update etc out of tests functions and into the class as
        # as members to avoid duplicating this part in all tests.
        default_doc_storage = {}

        def default_get(document_id: str):
            return default_doc_storage[document_id]

        def default_update(uid, data):
            default_doc_storage[uid] = data
            return None

        default_repo = mock.Mock()
        default_repo.name = "default"
        default_repo.data_types = [StorageDataTypes.DEFAULT]
        default_repo.get = default_get
        default_repo.update = default_update
        data_source_collection = mock.Mock()

        def mock_find_one(**kwargs):
            return None

        data_source_collection.find_one = mock_find_one
        data_source = DataSource(
            name="testing",
            user=test_user,
            repositories={"default": default_repo},
            data_source_collection=data_source_collection,
        )
        document_service = get_mock_document_service(lambda x, y: data_source, user=test_user)
        uncontained_doc_node: Node = tree_node_from_dict(
            document,
            uid="1",
            blueprint_provider=document_service.get_blueprint,
            recipe_provider=mock_storage_recipe_provider,
        )
        document_service.save(uncontained_doc_node, "testing", update_uncontained=True)

        # Test the "uncontained_in_every_way" attribute has been stored as a separate document in the document storage
        assert default_doc_storage and len(default_doc_storage.keys()) == 2 and default_doc_storage["1"]["uncontained_in_every_way"]["type"] == SIMOS.REFERENCE.value



    # TODO add a test for save in multiple repos (?)

    def test_save_based_on_root_storageRecipe(self):
        blob_doc = {"name": "some_entity", "description": "", "type": "blob", "someData": "test"}

        default_doc_storage = {}

        def default_get(document_id: str):
            return default_doc_storage[document_id]

        def default_update(uid, data):
            default_doc_storage[uid] = data
            return None

        blob_doc_storage = {}

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

        document_service = get_mock_document_service(lambda x, y: data_source, user=test_user)

        node: Node = tree_node_from_dict(
            blob_doc,
            uid="1",
            blueprint_provider=document_service.get_blueprint,
            recipe_provider=mock_storage_recipe_provider,
        )

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
            return default_doc_storage[document_id]

        def default_update(uid, data):
            default_doc_storage[uid] = data
            return None

        blob_doc_storage = {}

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

        document_service = get_mock_document_service(lambda x, y: data_source, user=test_user)

        node: Node = tree_node_from_dict(
            blob_doc, document_service.get_blueprint, uid="1", recipe_provider=mock_storage_recipe_provider
        )

        document_service.save(node, "testing", update_uncontained=True)

        # Test that both repos gets written into
        assert blob_doc_storage and default_doc_storage
