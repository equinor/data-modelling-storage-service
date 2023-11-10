import unittest

from domain_classes.blueprint_attribute import BlueprintAttribute
from features.entity.use_cases.instantiate_entity_use_case.create_entity import (
    CreateEntity,
)
from tests.unit.mocks.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mocks.mock_document_service import get_mock_document_service


class CreateEntityTestCase(unittest.TestCase):
    def setUp(self):
        simos_blueprints = [
            "dmss://system/SIMOS/AttributeTypes",
            "dmss://system/SIMOS/BlueprintAttribute",
            "dmss://system/SIMOS/Entity",
            "dmss://system/SIMOS/NamedEntity",
            "dmss://system/SIMOS/Blueprint",
        ]
        mock_blueprint_folder = "src/tests/unit/use_cases/instantiate_entity_use_case/mock_data/"
        mock_blueprints_and_file_names = {
            "CarTest": "CarTest.blueprint.json",
            "WheelTest": "WheelTest.blueprint.json",
            "EngineTest": "EngineTest.blueprint.json",
            "FuelPumpTest": "FuelPumpTest.blueprint.json",
        }
        self.mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
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
            "engine3": {
                "name": "default engine",
                "type": "EngineTest",
                "fuelPump": {"name": "fuelPump", "type": "FuelPumpTest", "description": "A standard fuel pump"},
                "power": 9,
            },
        }

        entity = CreateEntity(blueprint_provider=self.mock_document_service.get_blueprint, type="CarTest").entity

        self.assertDictEqual(expected_entity, entity)

    def test_create_default_blueprint(self):
        expected_entity = {
            "type": "dmss://system/SIMOS/Blueprint",
            "name": "",
            "attributes": [
                {
                    "name": "name",
                    "type": "dmss://system/SIMOS/BlueprintAttribute",
                    "attributeType": "string",
                    "optional": True,
                },
                {"name": "type", "type": "dmss://system/SIMOS/BlueprintAttribute", "attributeType": "string"},
                {
                    "name": "description",
                    "type": "dmss://system/SIMOS/BlueprintAttribute",
                    "attributeType": "string",
                    "optional": True,
                },
            ],
        }

        entity = CreateEntity(
            blueprint_provider=self.mock_document_service.get_blueprint, type="dmss://system/SIMOS/Blueprint"
        ).entity

        self.assertEqual(expected_entity, entity)

    def test_is_not_json(self):
        self.assertEqual(
            False,
            CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="string", default="")),
        )
        self.assertEqual(
            False,
            CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="string", default=" [] some")),
        )
        self.assertEqual(
            False,
            CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="boolean", default=False)),
        )
        self.assertEqual(
            False,
            CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="integer", default=123)),
        )
        self.assertEqual(
            False,
            CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="string", default="{'a': 123}")),
        )

    def test_is_json(self):
        self.assertEqual(
            True,
            CreateEntity.is_json(BlueprintAttribute(name="", attributeType="some", default=[], dimensions="*")),
        )
        self.assertEqual(
            True,
            CreateEntity.is_json(BlueprintAttribute(name="", attributeType="some", default=["a", "b"], dimensions="1")),
        )
        self.assertEqual(
            True,
            CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="some", default={"foo": "bar"})),
        )
