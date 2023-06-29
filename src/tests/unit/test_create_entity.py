import unittest

from common.utils.create_entity import CreateEntity
from domain_classes.blueprint_attribute import BlueprintAttribute
from storage.repositories.file import LocalFileRepository
from tests.unit.mock_utils import get_mock_document_service

file_repository_test = LocalFileRepository()

document_service = get_mock_document_service()
blueprint_provider = document_service.get_blueprint


class CreateEntityTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_blueprint_entity(self):
        expected_entity = {
            "engine": {
                "name": "",
                "description": "",
                "fuelPump": {
                    "name": "fuelPump",
                    "description": "A standard fuel pump",
                    "type": "test_data/complex/FuelPumpTest",
                },
                "power": 120,
                "type": "test_data/complex/EngineTest",
            },
            "engine3": {
                "name": "default engine",
                "fuelPump": {
                    "name": "fuelPump",
                    "description": "A standard fuel pump",
                    "type": "test_data/complex/FuelPumpTest",
                },
                "power": 9,
                "type": "test_data/complex/EngineTest",
            },
            "is_sedan": True,
            "name": "CarTest",
            "plateNumber": "",
            "seats": 2,
            "type": "test_data/complex/CarTest",
            "wheel": {"name": "Wheel", "power": 0.0, "type": "test_data/complex/WheelTest"},
            "wheels": [],
            "floatValues": [2.1, 3.1, 4.2],
            "intValues": [1, 5, 4, 2],
            "boolValues": [True, False, True],
            "stringValues": ["one", "two", "three"],
        }

        entity = CreateEntity(blueprint_provider=blueprint_provider, type="test_data/complex/CarTest").entity

        self.assertEqual(expected_entity, entity)

    def test_is_not_json(self):
        self.assertEqual(False, CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="string", default="")))
        self.assertEqual(
            False, CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="string", default=" [] some"))
        )
        self.assertEqual(
            False, CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="boolean", default=False))
        )
        self.assertEqual(
            False, CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="integer", default=123))
        )
        self.assertEqual(
            False, CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="string", default="{'a': 123}"))
        )

    def test_is_json(self):
        self.assertEqual(
            True, CreateEntity.is_json(BlueprintAttribute(name="", attributeType="some", default=[], dimensions="*"))
        )
        self.assertEqual(
            True,
            CreateEntity.is_json(
                BlueprintAttribute(name="", attributeType="some", default=["a", "b"], dimensions="1")
            ),
        )
        self.assertEqual(
            True, CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="some", default={"foo": "bar"}))
        )
