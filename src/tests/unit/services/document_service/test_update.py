import unittest
from copy import deepcopy
from unittest import mock

from common.address import Address
from common.tree.tree_node import Node
from tests.unit.mocks.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mocks.mock_document_service import get_mock_document_service
from tests.unit.mocks.mock_recipe_provider import MockStorageRecipeProvider


class DocumentServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        simos_blueprints = [
            "dmss://system/SIMOS/NamedEntity",
            "dmss://system/SIMOS/Entity",
            "dmss://system/SIMOS/Reference",
        ]
        mock_blueprint_folder = "src/tests/unit/services/document_service/mock_blueprints/car_rental_blueprints"
        mock_blueprints_and_file_names = {
            "FuelPumpTest": "FuelPumpTest.blueprint.json",
            "EngineTest": "EngineTest.blueprint.json",
        }
        self.mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        )
        recipe_provider = MockStorageRecipeProvider(
            "src/tests/unit/services/document_service/mock_blueprints/car_rental_blueprints/mock_storage_recipes.json"
        ).provider

        self.mock_document_service = get_mock_document_service(
            blueprint_provider=self.mock_blueprint_provider,
            recipe_provider=recipe_provider,
        )

    def test_update_partial_w_required_primitive(self):
        repository = mock.Mock()

        doc_storage: dict = {
            "1": {
                "_id": "1",
                "name": "myEngine",
                "description": "Some description",
                "fuelPump": {
                    "name": "fuelPump",
                    "description": "A standard fuel pump",
                    "type": "FuelPumpTest",
                },
                "power": 120,
                "type": "EngineTest",
            }
        }

        def mock_get(document_id: str):
            return deepcopy(doc_storage[document_id])

        def mock_update(entity: dict, *args, **kwargs):
            doc_storage[entity["_id"]] = entity
            return None

        repository.get = mock_get
        repository.update = mock_update

        self.mock_document_service.repository_provider = lambda *args: repository
        node: Node = self.mock_document_service.get_document(Address("$1", "testing"))
        node.update(
            {
                "_id": "1",
                "name": "ANOTHER NAME",
                "description": "New description",
                "type": "EngineTest",
            },
            True,
        )

        assert node.entity == {
            "_id": "1",
            "name": "ANOTHER NAME",
            "description": "New description",
            "fuelPump": {
                "name": "fuelPump",
                "description": "A standard fuel pump",
                "type": "FuelPumpTest",
            },
            "power": 120,
            "type": "EngineTest",
        }
