from collections.abc import Callable
from dataclasses import dataclass

from domain_classes.blueprint_attribute import BlueprintAttribute
from domain_classes.dependency import Dependency
from enums import PRIMITIVES


@dataclass(frozen=True)
class Meta:
    dependencies: list[Dependency]
    type: str = ""
    version: str = "0.0.1"


class Blueprint:
    def __init__(self, entity: dict, path: str | None = None):
        self.name = entity["name"]
        self.description = entity.get("description", "")
        self.meta: Meta = Meta(entity.get("_meta_"))  # type: ignore
        self.abstract = entity.get("abstract", False)
        self.extends = entity.get("extends", [])
        self.type = entity["type"]
        self.entity = entity
        self.attributes: list[BlueprintAttribute] = [
            BlueprintAttribute(**attribute) for attribute in entity.get("attributes", [])
        ]
        self.path = path

    @classmethod
    def from_dict(cls, adict):
        instance = cls(adict)
        instance.attributes = [BlueprintAttribute(**attr) for attr in adict.get("attributes", [])]
        return instance

    def get_required_attributes(self) -> list[BlueprintAttribute]:
        return [attribute for attribute in self.attributes if attribute.optional is False]

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "abstract": self.abstract,
            "extends": self.extends,
            "attributes": [attribute.to_dict() for attribute in self.attributes],
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __str__(self):
        return (
            f"Name: '{self.name}', Attributes: "
            f"{[f'{n}({self.get_attribute_type_by_key(n)})' for n in self.get_attribute_names()]}"
        )

    def get_none_primitive_types(self) -> list[BlueprintAttribute]:
        blueprints = [attribute for attribute in self.attributes if attribute.attribute_type not in PRIMITIVES]
        return blueprints

    def get_primitive_types(self) -> list[BlueprintAttribute]:
        # TODO function does not return the primitive types from the blueprint that self extends from (self.extends)
        blueprints = [attribute for attribute in self.attributes if attribute.attribute_type in PRIMITIVES]
        return blueprints

    def get_attribute_names(self) -> list[str]:
        return [attribute.name for attribute in self.attributes]

    def get_attribute_type_by_key(self, key):
        return next((attr.attribute_type for attr in self.attributes if attr.name == key), None)

    def get_attribute_by_name(self, key) -> BlueprintAttribute | None:
        return next((attr for attr in self.attributes if attr.name == key), None)

    def get_model_contained_by_name(self, key):
        return next((attr.contained for attr in self.attributes if attr.name == key), True)

    def is_attr_removable(self, attribute_name):
        for attr in self.attributes:
            if attr.name == attribute_name and not attr.is_primitive:
                if attr.is_array:
                    return False
                elif not attr.is_optional:
                    return False
        return True

    def realize_extends(self, blueprint_provider: Callable[[str], "Blueprint"]):
        """
        Recursive
        Inherits attributes, storage-, and ui-recipies from "extended" blueprints
        Overrides attributes with similar names from ancestor blueprints, except from DefaultStorageRecipe
        """
        new_attributes: dict[str, BlueprintAttribute] = {}

        for base in self.extends:
            base_blueprint: Blueprint = blueprint_provider(base)
            base_blueprint.realize_extends(blueprint_provider)
            # Overrides left. attribute names are CASE-INSENSITIVE
            # DefaultStorageRecipes does not override recipes from base
            new_attributes.update({attr.name.lower(): attr for attr in base_blueprint.attributes})

        new_attributes.update({attr.name.lower(): attr for attr in self.attributes})

        self.attributes = [attr for attr in new_attributes.values()]
