import unittest

from common.exceptions import ValidationException
from features.entity.use_cases.validate_entity import validate_entity
from tests.unit.mock_utils import get_mock_document_service


class ValidateEntityTestCase(unittest.TestCase):
    get_blueprint = get_mock_document_service().get_blueprint

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
                {"attributeType": "string", "type": "dmss://system/SIMOS/BlueprintAttribute", "name": "type"},
            ],
        }
        blueprint = self.get_blueprint(test_entity["type"])
        validate_entity(test_entity, blueprint, self.get_blueprint)

    def test_a_deeply_nested_valid_entity(self):
        test_entity = {
            "engine2": {},
            "engine": {
                "name": "myEngine",
                "description": "Some description",
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
        blueprint = self.get_blueprint(test_entity["type"])
        validate_entity(test_entity, blueprint, self.get_blueprint)

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
        blueprint = self.get_blueprint(test_entity["type"])
        with self.assertRaises(ValidationException) as error:
            validate_entity(test_entity, blueprint, self.get_blueprint)
        assert (
            error.exception.message
            == "Attributes '['do-not-belong']' are not specified in the 'dmss://system/SIMOS/BlueprintAttribute'"
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
        blueprint = self.get_blueprint(test_entity["type"])
        with self.assertRaises(ValidationException) as error:
            validate_entity(test_entity, blueprint, self.get_blueprint)
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
        blueprint = self.get_blueprint(test_entity["type"])
        with self.assertRaises(ValidationException) as error:
            validate_entity(test_entity, blueprint, self.get_blueprint)
        assert error.exception.message == "Attribute 'name' should be type 'str'. Got 'bool'"

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
        blueprint = self.get_blueprint(test_entity["type"])
        with self.assertRaises(ValidationException) as error:
            validate_entity(test_entity, blueprint, self.get_blueprint)
        assert error.exception.message == "Attribute 'name' should be type 'str'. Got 'list'"

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
        blueprint = self.get_blueprint(test_entity["type"])
        validate_entity(test_entity, blueprint, self.get_blueprint)

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
        blueprint = self.get_blueprint(test_entity["type"])
        with self.assertRaises(ValidationException) as error:
            validate_entity(test_entity, blueprint, self.get_blueprint)
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
                    "name": "",
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
            "floatValues": [2.1, 9999999.0, 4.2],
            "intValues": [1, 5, 4, 2],
            "boolValues": [True, False, True],
            "stringValues": ["one", "two", "three"],
        }
        blueprint = self.get_blueprint(test_entity["type"])
        with self.assertRaises(ValidationException) as error:
            validate_entity(test_entity, blueprint, self.get_blueprint)
        assert error.exception.message == "Missing required attribute 'name'"
        assert error.exception.debug == "Location: Entity in key '^.engine.name'"

    def test_an_entity_with_an_invalid_primitive_element_in_list(self):
        test_entity = {
            "engine2": {},
            "engine": {
                "name": "myEngine",
                "description": "Some description",
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
            "floatValues": [2.1, "string", 4.2],
            "intValues": [1, 5, 4, 2],
            "boolValues": [True, False, True],
            "stringValues": ["one", "two", "three"],
        }
        blueprint = self.get_blueprint(test_entity["type"])
        with self.assertRaises(ValidationException) as error:
            validate_entity(test_entity, blueprint, self.get_blueprint)
        assert error.exception.message == "Attribute 'floatValues' should be type 'float'. Got 'str'"
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
        blueprint = self.get_blueprint("dmss://system/SIMOS/Blueprint")
        validate_entity(test_entity, blueprint, self.get_blueprint, allow_extra=True)

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
            blueprint = self.get_blueprint("dmss://system/SIMOS/Blueprint")
            validate_entity(test_entity, blueprint, self.get_blueprint, allow_extra=True)
        assert error.exception.message == "Attribute 'attributeType' should be type 'str'. Got 'int'"
        assert error.exception.debug == "Location: Entity in key '^.attributes.0.attributeType'"
