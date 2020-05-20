from typing import Dict, List

from api.classes.blueprint_attribute import BlueprintAttribute
from api.core.enums import PRIMITIVES, StorageDataTypes

DEFAULT_PRIMITIVE_CONTAINED = True
DEFAULT_COMPLEX_CONTAINED = True


class StorageAttribute:
    def __init__(
        self,
        name: str,
        contained: bool = DEFAULT_PRIMITIVE_CONTAINED,
        storageTypeAffinity: str = StorageDataTypes.DEFAULT.value,
        label: str = "",
        description: str = "",
        **kwargs,
    ):
        self.name = name
        self.is_contained = contained
        self.type = "system/SIMOS/StorageAttribute"
        self.storage_type_affinity = StorageDataTypes(storageTypeAffinity)
        self.label = label
        self.description = description

    def __repr__(self):
        return f"name: {self.name}, contained: {self.is_contained}, optional: {self.storage_type_affinity}"

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "contained": self.is_contained,
            "type": self.type,
            "dataType": self.storage_type_affinity,
            "label": self.label,
            "description": self.description,
        }


class StorageRecipe:
    def __init__(self, name: str, attributes: List[Dict] = None):
        attributes = attributes if attributes else []
        self.name = name
        self.storage_attributes = {attribute["name"]: StorageAttribute(**attribute) for attribute in attributes}

    def is_contained(self, attribute_name, attribute_type=None):
        if attribute_name in self.storage_attributes:
            return self.storage_attributes[attribute_name].is_contained
        if attribute_type in PRIMITIVES:
            return DEFAULT_PRIMITIVE_CONTAINED
        else:
            return DEFAULT_COMPLEX_CONTAINED

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "attributes": [attribute.to_dict() for attribute in self.storage_attributes],
        }

    def none_contained_attributes(self) -> List[str]:
        return [attr.name for attr in self.storage_attributes if not attr.is_contained]


class DefaultStorageRecipe(StorageRecipe):
    def __init__(self, attributes: List[BlueprintAttribute]):
        super().__init__("Default")
        self.storage_attributes = {
            attribute.name: StorageAttribute(name=attribute.name, contained=attribute.contained)
            for attribute in attributes
        }
