import json
from collections.abc import Callable
from json import JSONDecodeError

from domain_classes.blueprint import Blueprint
from domain_classes.blueprint_attribute import BlueprintAttribute
from enums import PRIMITIVES, SIMOS, BuiltinDataTypes
from features.entity.use_cases.instantiate_entity_use_case.create_entity_arrays import (
    create_default_array,
)


class CreateEntity:
    """
    Rules for creating an entity of a given blueprint type:
    - all required attributes, as defined in the blueprint, are included.
      If the required attribute has a default value, that value will be used.
      If not, an 'empty' value will be used. For example empty string,
      an empty list, the number 0, etc.
    - optional attributes value are not included (also true if default value is provided).
    """

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
                return create_default_array(attr.dimensions, blueprint_provider, CreateEntity)
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

    # type is inserted based on the parent attributes type, or the initial type for root entity.
    def _get_entity(self, blueprint: Blueprint, entity: dict):
        for attr in blueprint.attributes:
            if attr.attribute_type == BuiltinDataTypes.BINARY.value:
                continue
            if attr.is_optional and not attr.default:
                # skip attribute if it is optional
                continue
            if attr.attribute_type in PRIMITIVES:
                if attr.name not in entity:
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
                    entity[attr.name] = create_default_array(
                        attr.dimensions,
                        self.blueprint_provider,
                        CreateEntity,
                        attr.default,
                    )
                else:
                    if CreateEntity.is_json(attr):
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
