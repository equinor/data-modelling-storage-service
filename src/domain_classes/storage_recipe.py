from pydantic import BaseModel, Field

from enums import PRIMITIVES, SIMOS, StorageDataTypes

DEFAULT_PRIMITIVE_CONTAINED = True
DEFAULT_COMPLEX_CONTAINED = True


class StorageAttribute(BaseModel):
    name: str
    type: str = SIMOS.STORAGE_ATTRIBUTE.value
    contained: bool = DEFAULT_PRIMITIVE_CONTAINED
    storage_affinity: StorageDataTypes = Field(StorageDataTypes.DEFAULT, alias="storageAffinity")
    label: str = ""
    description: str = ""

    def __repr__(self):
        return f"name: {self.name}, contained: {self.contained}, affinity: {self.storage_affinity.value}"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "contained": self.contained,
            "type": self.type,
            "storageAffinity": self.storage_affinity.value,
            "label": self.label,
            "description": self.description,
        }

    class Config:
        allow_population_by_field_name = True


class StorageRecipe(BaseModel):
    name: str
    type: str = SIMOS.STORAGE_RECIPE.value
    attributes: dict[str, StorageAttribute] = {}
    storage_affinity: StorageDataTypes = Field(StorageDataTypes.DEFAULT, alias="storageAffinity")
    description: str = ""

    class Config:
        allow_population_by_field_name = True

    def is_contained(self, attribute_name, attribute_type=None):
        if attribute_name in self.attributes:
            return self.attributes[attribute_name].contained
        if attribute_type in PRIMITIVES:
            return DEFAULT_PRIMITIVE_CONTAINED

        return DEFAULT_COMPLEX_CONTAINED

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "storageAffinity": self.storage_affinity.value,
            "attributes": [attribute.to_dict() for attribute in self.attributes.values()],
        }

    def none_contained_attributes(self) -> list[str]:
        return [attr.name for attr in self.attributes.values() if not attr.contained]
