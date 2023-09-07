import unittest
from unittest import mock

from common.address import Address
from common.utils.data_structure.compare import get_and_print_diff
from domain_classes.blueprint import Blueprint
from domain_classes.tree_node import Node
from tests.unit.mock_data.mock_document_service import get_mock_document_service


class GetExtendedBlueprintTestCase(unittest.TestCase):
    def test_get_simple_extended(self):
        document_service = get_mock_document_service()
        full_blueprint: Blueprint = document_service.get_blueprint("ExtendedBlueprint")

        assert next((attr for attr in full_blueprint.attributes if attr.name == "description"), None) is not None

    def test_get_second_level_extended(self):
        document_service = get_mock_document_service()
        full_blueprint: Blueprint = document_service.get_blueprint("SecondLevelExtendedBlueprint")

        assert next((attr for attr in full_blueprint.attributes if attr.name == "description"), None) is not None
        assert next((attr for attr in full_blueprint.attributes if attr.name == "another_value"), None) is not None
        assert next((attr for attr in full_blueprint.attributes if attr.name == "a_third_value"), None) is not None

    def test_updated_extended_entity(self):
        repository = mock.Mock()

        doc_storage = {
            "1": {
                "_id": "1",
                "name": "HalloExtendedWorld",
                "description": "",
                "type": "SecondLevelExtendedBlueprint",
                "another_value": "amastring",
                "a_third_value": "amanothastring",
            }
        }

        doc_1_after = {
            "_id": "1",
            "name": "HalloExtendedWorld",
            "description": "",
            "type": "SecondLevelExtendedBlueprint",
            "another_value": "I CHANGED",
            "a_third_value": "amanothastring",
        }

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity

        repository.get = lambda doc_id: doc_storage[doc_id]
        repository.update = mock_update
        document_service = get_mock_document_service(lambda x, y: repository)

        node: Node = document_service.get_document(Address.from_absolute("testing/$1"))
        node.update(doc_1_after)
        document_service.save(node, "testing")

        assert get_and_print_diff(doc_storage["1"], doc_1_after) == []
