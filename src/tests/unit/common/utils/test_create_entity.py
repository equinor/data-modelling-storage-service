import unittest

from common.utils.create_entity import CreateEntity
from domain_classes.blueprint_attribute import BlueprintAttribute
from tests.unit.mock_data.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mock_data.mock_document_service import get_mock_document_service


class CreateEntityTestCase(unittest.TestCase):
    def setUp(self):
        simos_blueprints = [
            "dmss://system/SIMOS/AttributeTypes",
            "dmss://system/SIMOS/BlueprintAttribute",
            "dmss://system/SIMOS/NamedEntity",
        ]
        mock_blueprint_folder = "src/tests/unit/mock_data/mock_blueprints"
        self.mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprint_folder=mock_blueprint_folder, simos_blueprints_available_for_test=simos_blueprints
        )
        self.mock_document_service = get_mock_document_service(blueprint_provider=self.mock_blueprint_provider)
        self.maxDiff = None

    def test_blueprint_entity(self):
        expected_entity = {
            "engine": {
                "name": "",
                "description": "",
                "fuelPump": {
                    "name": "fuelPump",
                    "description": "A standard fuel pump",
                    "type": "FuelPumpTest",
                },
                "power": 120,
                "type": "EngineTest",
            },
            "is_sedan": True,
            "name": "CarTest",
            "plateNumber": "",
            "seats": 2,
            "type": "CarTest",
            "wheel": {"name": "Wheel", "power": 0.0, "type": "WheelTest"},
            "wheels": [],
            "floatValues": [2.1, 3.1, 4.2],
            "intValues": [1, 5, 4, 2],
            "boolValues": [True, False, True],
            "stringValues": ["one", "two", "three"],
        }

        entity = CreateEntity(blueprint_provider=self.mock_document_service.get_blueprint, type="CarTest").entity

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
