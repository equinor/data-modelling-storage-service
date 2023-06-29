import json
from json import JSONDecodeError
from typing import Callable

from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from enums import PRIMITIVES, SIMOS, BuiltinDataTypes


class CreateEntityException(Exception):
    def __init__(self, message: str):
        super()
        self.message = message

    def __str__(self):
        return repr(self.message)


class InvalidDefaultValue(CreateEntityException):
    def __init__(self, attr: BlueprintAttribute, blueprint_name: str):
        super().__init__(message=f"blueprint: {blueprint_name}, attribute: {attr.name} has empty default value.")


class CreateEntity:
    def __init__(self, blueprint_provider: Callable, type: str):
        if type == BuiltinDataTypes.OBJECT.value:
            type = SIMOS.ENTITY.value
        self.type = type
        self.blueprint_provider = blueprint_provider
        self.attribute_types = self.blueprint_provider(SIMOS.ATTRIBUTE_TYPES.value).to_dict()
        self.blueprint_attribute: Blueprint = self.blueprint_provider(SIMOS.BLUEPRINT_ATTRIBUTE.value)
        blueprint: Blueprint = self.blueprint_provider(type)
        entity = {"type": type}
        self._entity = self._get_entity(blueprint=blueprint, entity=entity)

    @staticmethod
    def parse_value(attr: BlueprintAttribute, blueprint_provider):
        default_value = attr.default
        type = attr.attribute_type

        if default_value is not None and len(str(default_value)) > 0 and attr.is_array and type not in PRIMITIVES:
            try:
                return json.loads(default_value)
            except JSONDecodeError:
                print(f"invalid default value: {default_value} for attribute: {attr}")
                return []

        if default_value is None:
            if attr.is_array:
                return attr.dimensions.create_default_array(blueprint_provider, attr)
            if type == "boolean":
                return False
            if type == "number":
                return 0.0
            if type == "integer":
                return 0
            if type == "string":
                return ""
        return default_value

    @property
    def entity(self):
        return self._entity

    @staticmethod
    def is_json(attr: BlueprintAttribute):
        """A blueprint attribute is json if the default value is either a list or a dict."""
        return attr.attribute_type not in PRIMITIVES or attr.dimensions.dimensions != [
            ""
        ]  # type(attr.default) == dict or type(attr.default) == list

    # add all non optional attributes with default value.
    # type is inserted based on the parent attributes type, or the initial type for root entity.
    def _get_entity(self, blueprint: Blueprint, entity: dict):
        for attr in blueprint.attributes:
            if attr.attribute_type == BuiltinDataTypes.BINARY.value:
                continue

            if attr.attribute_type in PRIMITIVES:
                if not attr.is_optional and attr.name not in entity:
                    entity[attr.name] = CreateEntity.parse_value(attr=attr, blueprint_provider=self.blueprint_provider)
            else:
                blueprint = (
                    self.blueprint_provider(attr.attribute_type)
                    if (
                        attr.attribute_type != BuiltinDataTypes.OBJECT.value
                        and attr.attribute_type != BuiltinDataTypes.BINARY.value
                    )
                    else self.blueprint_provider(SIMOS.ENTITY.value)
                )
                if attr.is_array:
                    entity[attr.name] = attr.dimensions.create_default_array(self.blueprint_provider, CreateEntity)
                else:
                    if attr.is_optional:
                        if attr.default:
                            entity[attr.name] = attr.default
                    elif CreateEntity.is_json(attr):
                        value = attr.default
                        if value is not None and len(value) > 0:
                            entity[attr.name] = attr.default
                        else:
                            entity[attr.name] = self._get_entity(
                                blueprint=blueprint, entity={"type": attr.attribute_type}
                            )
                    else:
                        entity[attr.name] = self._get_entity(blueprint=blueprint, entity={"type": attr.attribute_type})
        return entity
