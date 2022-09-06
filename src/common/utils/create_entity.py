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

        if default_value is not None and len(str(default_value)) > 0 and attr.is_array():
            try:
                return json.loads(default_value)
            except JSONDecodeError:
                print(f"invalid default value: {default_value} for attribute: {attr}")
                return []

        if default_value == "":
            if attr.is_array():
                return attr.dimensions.create_default_array(blueprint_provider, attr)
            if type == "boolean":
                return False
            if type == "number":
                return 0.0
            if type == "integer":
                return 0

        if type == "boolean":
            return bool(default_value)
        if type == "number":
            return float(default_value)
        if type == "integer":
            return int(default_value)
        return default_value

    @property
    def entity(self):
        return self._entity

    @staticmethod
    def is_json(attr: BlueprintAttribute):
        try:
            json.loads(attr.default)
            return True
        except JSONDecodeError:
            return False
        except StopIteration:
            return False

    @staticmethod
    def parse_json(attr: BlueprintAttribute):
        try:
            return json.loads(attr.default)
        except JSONDecodeError:
            print(f"invalid default value: {attr.default} for attribute: {attr}")
            return ""

    # add all non optional attributes with default value.
    # type is inserted based on the parent attributes type, or the initial type for root entity.
    def _get_entity(self, blueprint: Blueprint, entity):
        for attr in blueprint.attributes:
            if attr.attribute_type in PRIMITIVES:
                if not attr.is_optional() and attr.name not in entity:
                    entity[attr.name] = CreateEntity.parse_value(attr=attr, blueprint_provider=self.blueprint_provider)
            else:
                blueprint = (
                    self.blueprint_provider(attr.attribute_type)
                    if attr.attribute_type != BuiltinDataTypes.OBJECT.value
                    else SIMOS.ENTITY.value
                )
                if attr.is_array():
                    entity[attr.name] = attr.dimensions.create_default_array(self.blueprint_provider, CreateEntity)
                else:
                    if attr.is_optional():
                        entity[attr.name] = {}

                    elif CreateEntity.is_json(attr):
                        value = CreateEntity.parse_json(attr)
                        if len(value) > 0:
                            entity[attr.name] = CreateEntity.parse_json(attr)
                        else:
                            entity[attr.name] = self._get_entity(
                                blueprint=blueprint, entity={"type": attr.attribute_type}
                            )
                    else:
                        entity[attr.name] = self._get_entity(blueprint=blueprint, entity={"type": attr.attribute_type})
        return entity
