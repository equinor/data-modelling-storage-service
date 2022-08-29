import unittest

from common.utils.create_entity import CreateEntity
from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from services.document_service import DocumentService
from storage.repositories.file import LocalFileRepository

file_repository_test = LocalFileRepository()


class BlueprintProvider:
    def get_blueprint(self, template_type: str):
        if template_type == "test_data/complex/FuelPumpTest":
            return Blueprint(
                {
                    "type": "system/SIMOS/Blueprint",
                    "name": "FuelPumpTest",
                    "description": "This describes a fuel pump",
                    "attributes": [
                        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
                        {
                            "attributeType": "string",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "name": "description",
                            "default": "A standard fuel pump",
                        },
                        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
                    ],
                }
            )
        if template_type == "test_data/complex/EngineTest":
            return Blueprint(
                {
                    "type": "system/SIMOS/Blueprint",
                    "name": "EngineTest",
                    "description": "This describes an engine",
                    "attributes": [
                        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
                        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
                        {
                            "attributeType": "string",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "name": "description",
                        },
                        {
                            "attributeType": "integer",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "name": "power",
                            "default": "120",
                        },
                        {
                            "type": "system/SIMOS/BlueprintAttribute",
                            "attributeType": "test_data/complex/FuelPumpTest",
                            "name": "fuelPump",
                            "default": '{"description":"A standard fuel pump","name":"fuelPump","type":"test_data/complex/FuelPumpTest"}',
                        },
                    ],
                }
            )
        if template_type == "test_data/complex/CarTest":
            return Blueprint(
                {
                    "type": "system/SIMOS/Blueprint",
                    "name": "CarTest",
                    "attributes": [
                        {
                            "name": "name",
                            "attributeType": "string",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "default": "CarTest",
                        },
                        {
                            "name": "type",
                            "attributeType": "string",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "default": "test_data/complex/CarTest",
                        },
                        {
                            "type": "system/SIMOS/BlueprintAttribute",
                            "name": "wheel",
                            "attributeType": "test_data/complex/WheelTest",
                        },
                        {
                            "type": "system/SIMOS/BlueprintAttribute",
                            "name": "wheels",
                            "attributeType": "test_data/complex/WheelTest",
                            "dimensions": "*",
                        },
                        {
                            "name": "seats",
                            "attributeType": "integer",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "default": "2",
                        },
                        {
                            "name": "is_sedan",
                            "attributeType": "boolean",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "default": "true",
                        },
                        {
                            "name": "floatValues",
                            "attributeType": "number",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "dimensions": "*",
                            "default": "[2.1,3.1,4.2]",
                        },
                        {
                            "name": "intValues",
                            "attributeType": "integer",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "dimensions": "*",
                            "default": "[1,5,4,2]",
                        },
                        {
                            "name": "boolValues",
                            "attributeType": "boolean",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "dimensions": "*",
                            "default": "[true, false, true]",
                        },
                        {
                            "name": "stringValues",
                            "attributeType": "string",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "dimensions": "*",
                            "default": '["one", "two", "three"]',
                        },
                        {
                            "type": "system/SIMOS/BlueprintAttribute",
                            "name": "engine",
                            "attributeType": "test_data/complex/EngineTest",
                        },
                        {
                            "type": "system/SIMOS/BlueprintAttribute",
                            "name": "engine2",
                            "optional": True,
                            "attributeType": "test_data/complex/EngineTest",
                        },
                    ],
                }
            )
        if template_type == "test_data/complex/WheelTest":
            return Blueprint(
                {
                    "name": "WheelTest",
                    "type": "system/SIMOS/Blueprint",
                    "attributes": [
                        {
                            "name": "name",
                            "attributeType": "string",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "default": "Wheel",
                        },
                        {"name": "type", "attributeType": "string", "type": "system/SIMOS/BlueprintAttribute"},
                        {
                            "name": "power",
                            "attributeType": "number",
                            "type": "system/SIMOS/BlueprintAttribute",
                            "default": "0.0",
                        },
                    ],
                }
            )
        return Blueprint(file_repository_test.get(template_type))


document_service = DocumentService(repository_provider=None, blueprint_provider=BlueprintProvider())
blueprint_provider = document_service.get_blueprint


class CreateEntityTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_blueprint_entity(self):
        expected_entity = {
            "engine2": {},
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
            "is_sedan": True,
            "name": "CarTest",
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
        self.assertEqual(False, CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="some", default="")))
        self.assertEqual(
            False, CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="some", default=" [] some"))
        )

    def test_is_json(self):
        self.assertEqual(True, CreateEntity.is_json(BlueprintAttribute(name="", attributeType="some", default=" [] ")))
        self.assertEqual(
            True, CreateEntity.is_json(BlueprintAttribute(name="", attribute_type="some", default=' {"foo": "bar"} '))
        )
