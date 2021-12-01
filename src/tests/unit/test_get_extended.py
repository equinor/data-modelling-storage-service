import unittest
from unittest import mock

from domain_classes.blueprint import Blueprint
from domain_classes.dto import DTO
from domain_classes.storage_recipe import StorageRecipe
from domain_classes.tree_node import Node
from domain_classes.ui_recipe import Recipe
from enums import StorageDataTypes
from services.document_service import DocumentService
from tests.unit.mock_blueprint_provider import blueprint_provider
from utils.data_structure.compare import pretty_eq


class GetExtendedBlueprintTestCase(unittest.TestCase):
    def test_get_simple_extended(self):
        document_service = DocumentService(repository_provider=None, blueprint_provider=blueprint_provider)
        full_blueprint: Blueprint = document_service.get_blueprint("ExtendedBlueprint")

        assert next((attr for attr in full_blueprint.attributes if attr.name == "description"), None) is not None

    def test_get_second_level_extended(self):
        document_service = DocumentService(repository_provider=None, blueprint_provider=blueprint_provider)
        full_blueprint: Blueprint = document_service.get_blueprint("SecondLevelExtendedBlueprint")

        assert next((attr for attr in full_blueprint.attributes if attr.name == "description"), None) is not None
        assert next((attr for attr in full_blueprint.attributes if attr.name == "another_value"), None) is not None
        assert next((attr for attr in full_blueprint.attributes if attr.name == "a_third_value"), None) is not None

    def test_extended_storage_and_ui_recipes_and_override(self):
        document_service = DocumentService(repository_provider=None, blueprint_provider=blueprint_provider)
        full_blueprint: Blueprint = document_service.get_blueprint("SecondLevelExtendedBlueprint")

        default_storage: StorageRecipe = next(
            (attr for attr in full_blueprint.storage_recipes if attr.name == "default"), None
        )
        assert default_storage.storage_affinity == StorageDataTypes.BLOB
        default_ui: Recipe = next((attr for attr in full_blueprint.ui_recipes if attr.name == "default"), None)
        special_ui: Recipe = next((attr for attr in full_blueprint.ui_recipes if attr.name == "aSpecialView"), None)
        assert default_ui.plugin == "edit2"
        assert special_ui.plugin == "specialView"

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

        def mock_update(dto: DTO, *args, **kwargs):
            doc_storage[dto.uid] = dto.data

        repository.get = lambda doc_id: DTO(doc_storage[doc_id])
        repository.update = mock_update
        document_service = DocumentService(
            blueprint_provider=blueprint_provider, repository_provider=lambda x, y: repository
        )

        node: Node = document_service.get_node_by_uid("testing", "1")
        node.update(doc_1_after)
        document_service.save(node, "testing")

        assert pretty_eq(doc_1_after, doc_storage["1"]) is None
