import unittest

from common.entity.validators import validate_entity, validate_entity_against_self
from common.exceptions import ValidationException
from common.tree.tree_node_serializer import tree_node_from_dict, tree_node_to_dict
from tests.unit.mock_data.mock_blueprint_provider import MockBlueprintProvider
from tests.unit.mock_data.mock_document_service import get_mock_document_service
from tests.unit.mock_data.mock_recipe_provider import MockStorageRecipeProvider


class ValidateEntityTestCase(unittest.TestCase):
    def setUp(self) -> None:
        simos_blueprints = [
            "dmss://system/SIMOS/Blueprint",
            "dmss://system/SIMOS/NamedEntity",
            "dmss://system/SIMOS/BlueprintAttribute",
        ]
        mock_blueprint_folder = "src/tests/unit/common/entity/validators/mock_data"
        mock_blueprints_and_file_names = {
            "CarRental": "CarRental.blueprint.json",
            "RentalCar": "RentalCar.blueprint.json",
            "CarTest": "CarTest.blueprint.json",
            "BaseChild": "BaseChild.blueprint.json",
            "WheelTest": "WheelTest.blueprint.json",
            "SpecialChild": "SpecialChild.blueprint.json",
            "Parent": "Parent.blueprint.json",
            "FuelPumpTest": "FuelPumpTest.blueprint.json",
            "EngineTest": "EngineTest.blueprint.json",
        }
        mock_blueprint_provider = MockBlueprintProvider(
            mock_blueprints_and_file_names=mock_blueprints_and_file_names,
            mock_blueprint_folder=mock_blueprint_folder,
            simos_blueprints_available_for_test=simos_blueprints,
        )

        self.recipe_provider = MockStorageRecipeProvider(
            "src/tests/unit/mock_data/mock_storage_recipes/mock_storage_recipes.json"
        ).provider

        self.mock_document_service = get_mock_document_service(blueprint_provider=mock_blueprint_provider)

    def test_a_simple_valid_entity(self):
        test_entity = {
            "type": "dmss://system/SIMOS/Blueprint",
            "name": "FuelPumpTest",
            "description": "This describes a fuel pump",
            "attributes": [
                {"attributeType": "string", "type": "dmss://system/SIMOS/BlueprintAttribute", "name": "name"},
                {
                    "attributeType": "string",
                    "type": "dmss://system/SIMOS/BlueprintAttribute",
                    "name": "description",
                    "default": "A standard fuel pump",
                },
                {
                    "attributeType": "number",
                    "type": "dmss://system/SIMOS/BlueprintAttribute",
                    "name": "a_number",
                    "default": 3,
                },
                {
                    "attributeType": "boolean",
                    "type": "dmss://system/SIMOS/BlueprintAttribute",
                    "name": "a_list",
                    "dimensions": "*",
                    "default": [True, False],
                },
                {"attributeType": "string", "type": "dmss://system/SIMOS/BlueprintAttribute", "name": "type"},
            ],
        }
        validate_entity_against_self(test_entity, self.mock_document_service.get_blueprint)

    def test_a_deeply_nested_valid_entity(self):
        test_entity = {
            "engine2": {},
            "engine": {
                "name": "myEngine",
                "description": "Some description",
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
            "plateNumber": "VH123456",
            "seats": 2,
            "type": "CarTest",
            "wheel": {"name": "Wheel", "power": 0.0, "type": "WheelTest"},
            "wheels": [],
            "floatValues": [2.1, 3.1, 0, 5, 99999123123],
            "intValues": [1, 5, 4, 2],
            "boolValues": [True, False, True],
            "stringValues": ["one", "two", "three"],
        }
        validate_entity_against_self(test_entity, self.mock_document_service.get_blueprint)

    def test_an_entity_with_an_attribute_which_does_not_belong(self):
        test_entity = {
            "type": "dmss://system/SIMOS/Blueprint",
            "name": "FuelPumpTest",
            "description": "This describes a fuel pump",
            "attributes": [
                {
                    "attributeType": "string",
                    "type": "dmss://system/SIMOS/BlueprintAttribute",
                    "name": "name",
                    "do-not-belong": 123,
                },
                {
                    "attributeType": "string",
                    "type": "dmss://system/SIMOS/BlueprintAttribute",
                    "name": "description",
                    "default": "A standard fuel pump",
                },
                {"attributeType": "string", "type": "dmss://system/SIMOS/BlueprintAttribute", "name": "type"},
            ],
        }
        with self.assertRaises(ValidationException) as error:
            validate_entity_against_self(test_entity, self.mock_document_service.get_blueprint)
        assert (
            error.exception.message
            == "Attributes '['do-not-belong']' are not specified in the blueprint 'dmss://system/SIMOS/BlueprintAttribute'"
        )

    def test_an_entity_with_a_missing_required_attribute(self):
        test_entity = {
            "type": "dmss://system/SIMOS/Blueprint",
            "description": "This describes a fuel pump",
            "attributes": [
                {"attributeType": "string", "type": "dmss://system/SIMOS/BlueprintAttribute", "name": "name"},
                {
                    "attributeType": "string",
                    "type": "dmss://system/SIMOS/BlueprintAttribute",
                    "name": "description",
                    "default": "A standard fuel pump",
                },
                {"attributeType": "string", "type": "dmss://system/SIMOS/BlueprintAttribute", "name": "type"},
            ],
        }
        with self.assertRaises(ValidationException) as error:
            validate_entity_against_self(test_entity, self.mock_document_service.get_blueprint)
        assert error.exception.message == "Missing required attribute 'name'"

    def test_an_entity_with_a_wrong_primitive_typed_value(self):
        test_entity = {
            "type": "dmss://system/SIMOS/Blueprint",
            "name": "FuelPump",
            "description": "This describes a fuel pump",
            "attributes": [
                {"attributeType": "string", "type": "dmss://system/SIMOS/BlueprintAttribute", "name": "name"},
                {
                    "attributeType": "string",
                    "type": "dmss://system/SIMOS/BlueprintAttribute",
                    "name": True,
                    "default": "A standard fuel pump",
                },
                {"attributeType": "string", "type": "dmss://system/SIMOS/BlueprintAttribute", "name": "type"},
            ],
        }
        with self.assertRaises(ValidationException) as error:
            validate_entity_against_self(test_entity, self.mock_document_service.get_blueprint)
        assert error.exception.message == "Attribute 'name' should be type 'str'. Got 'bool'. Value: True"

    def test_an_entity_with_a_wrong_typed_value_that_is_list(self):
        test_entity = {
            "type": "dmss://system/SIMOS/Blueprint",
            "name": "FuelPump",
            "description": "This describes a fuel pump",
            "attributes": [
                {"attributeType": "string", "type": "dmss://system/SIMOS/BlueprintAttribute", "name": "name"},
                {
                    "attributeType": "string",
                    "type": "dmss://system/SIMOS/BlueprintAttribute",
                    "name": ["this", "is", "wrong"],
                    "default": "A standard fuel pump",
                },
                {"attributeType": "string", "type": "dmss://system/SIMOS/BlueprintAttribute", "name": "type"},
            ],
        }
        with self.assertRaises(ValidationException) as error:
            validate_entity_against_self(test_entity, self.mock_document_service.get_blueprint)
        assert (
            error.exception.message
            == "Attribute 'name' should be type 'str'. Got 'list'. Value: ['this', 'is', 'wrong']"
        )

    def test_an_entity_with_a_valid_inherited_complex_type(self):
        test_entity = {
            "type": "Parent",
            "name": "parentEntity",
            "description": "",
            "SomeChild": {
                "name": "specialChildInParent2",
                "type": "SpecialChild",
                "description": "This type inherit the 'BaseChild' type",
                "AValue": 222,
                "AnExtraValue": "extra value",
            },
        }
        validate_entity_against_self(test_entity, self.mock_document_service.get_blueprint)

    def test_an_entity_with_a_wrong_typed_complex_value(self):
        test_entity = {
            "type": "Parent",
            "name": "parentEntity",
            "description": "",
            "SomeChild": {
                "name": "specialChildInParent2",
                "type": "dmss://system/SIMOS/Blueprint",
                "description": "I should not be a blueprint...",
                "AValue": 222,
                "AnExtraValue": "extra value",
            },
        }
        with self.assertRaises(ValidationException) as error:
            validate_entity_against_self(test_entity, self.mock_document_service.get_blueprint)
        assert (
            error.exception.message
            == "Entity should be of type 'BaseChild' (or extending from it). Got 'dmss://system/SIMOS/Blueprint'"
        )
        assert error.exception.debug == "Location: Entity in key '^.SomeChild'"

    def test_an_invalid_deeply_nested_entity(self):
        test_entity = {
            "engine2": {},
            "engine": {
                "name": "",
                "description": "",
                "fuelPump": {
                    "description": "A standard fuel pump",
                    "type": "FuelPumpTest",
                },
                "power": 120,
                "type": "EngineTest",
            },
            "is_sedan": True,
            "name": "CarTest",
            "plateNumber": "VH12345",
            "seats": 2,
            "type": "CarTest",
            "wheel": {"name": "Wheel", "power": 0.0, "type": "WheelTest"},
            "wheels": [],
            "floatValues": [2.1, 9999999.0, 4.2],
            "intValues": [1, 5, 4, 2],
            "boolValues": [True, False, True],
            "stringValues": ["one", "two", "three"],
        }
        with self.assertRaises(ValidationException) as error:
            validate_entity_against_self(test_entity, self.mock_document_service.get_blueprint)
        assert error.exception.message == "Missing required attribute 'name'"
        assert error.exception.debug == "Location: Entity in key '^.engine.fuelPump'"

    def test_array_with_complex_child_getting_array_type_from_parent_node(self):
        test_entity = {
            "_id": "2",
            "type": "CarRental",
            "name": "myCarRental",
            "cars": [
                {
                    "type": "RentalCar",
                    "name": "Volvo 240",
                    "plateNumber": "123",
                    "engine": {
                        "name": "myEngine",
                        "description": "Some description",
                        "fuelPump": {
                            "name": "fuelPump",
                            "description": "A standard fuel pump",
                            "type": "FuelPumpTest",
                        },
                        "power": 120,
                        "type": "EngineTest",
                    },
                },
            ],
            "customers": [],
        }

        parent_node = tree_node_from_dict(
            test_entity,
            self.mock_document_service.get_blueprint,
            recipe_provider=self.recipe_provider,
        )
        new_node = parent_node.get_by_path(["cars"])
        blueprint = new_node.blueprint

        validate_entity(
            tree_node_to_dict(new_node),
            self.mock_document_service.get_blueprint,
            blueprint,
            implementation_mode="exact",
        )

    def test_an_entity_with_an_invalid_primitive_element_in_list(self):
        test_entity = {
            "engine2": {},
            "engine": {
                "name": "myEngine",
                "description": "Some description",
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
            "plateNumber": "VH12345",
            "seats": 2,
            "type": "CarTest",
            "wheel": {"name": "Wheel", "power": 0.0, "type": "WheelTest"},
            "wheels": [],
            "floatValues": [2.1, "string", 4.2],
            "intValues": [1, 5, 4, 2],
            "boolValues": [True, False, True],
            "stringValues": ["one", "two", "three"],
        }
        with self.assertRaises(ValidationException) as error:
            validate_entity_against_self(test_entity, self.mock_document_service.get_blueprint)
        assert error.exception.message == "Attribute 'floatValues' should be type 'float'. Got 'str'. Value: string"
        assert error.exception.debug == "Location: Entity in key '^.floatValues.1'"

    def test_validate_against_base_type_not_inherited(self):
        test_entity = {
            "type": "something else that should not matter...",
            "name": "MyBlueprint",
            "description": "A descsription",
            "attributes": [
                {"attributeType": "string", "type": "dmss://system/SIMOS/BlueprintAttribute", "name": "name"},
            ],
            "anExtraParameter": {"whatEver": 123, "bla": "bla", "not validated": [[[]]]},
        }

        # Validate against the master blueprint
        blueprint = self.mock_document_service.get_blueprint("dmss://system/SIMOS/Blueprint")
        validate_entity(test_entity, self.mock_document_service.get_blueprint, blueprint, "minimum")

    def test_validate_against_base_type_not_inherited_invalid(self):
        test_entity = {
            "type": "something else that should not matter...",
            "name": "MyBlueprint",
            "description": "A descsription",
            "attributes": [
                {"attributeType": 132, "type": "dmss://system/SIMOS/BlueprintAttribute", "name": "name"},
            ],
            "anExtraParameter": {"whatEver": 123, "bla": "bla", "not validated": [[[]]]},
        }
        with self.assertRaises(ValidationException) as error:
            # Validate against the master blueprint
            blueprint = self.mock_document_service.get_blueprint("dmss://system/SIMOS/Blueprint")
            validate_entity(test_entity, self.mock_document_service.get_blueprint, blueprint, "minimum")
        assert error.exception.message == "Attribute 'attributeType' should be type 'str'. Got 'int'. Value: 132"
        assert error.exception.debug == "Location: Entity in key '^.attributes.0.attributeType'"
