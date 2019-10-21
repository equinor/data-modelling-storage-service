from typing import List

DEFAULT_PRIMITIVE_CONTAINED = True
DEFAULT_COMPLEX_CONTAINED = False
PRIMITIVES = ["string", "number", "integer", "boolean"]


class UIAttribute:
    def __init__(self, name: str, is_contained: bool = DEFAULT_PRIMITIVE_CONTAINED):
        self.name = name
        self.is_contained = is_contained


class UIRecipe:
    def __init__(self, name: str, attributes: List = None):
        self.name = name
        self.ui_attributes = {}
        if attributes:
            self._convert_attributes(attributes)

    def _convert_attributes(self, attributes):
        for attribute in attributes:
            print(attribute)
            self.ui_attributes[attribute["name"]] = UIAttribute(
                name=attribute["name"], is_contained=attribute.get("contained", True)
            )

    def is_contained(self, attribute):
        attribute_name = attribute["name"]
        attribute_type = attribute["type"]
        attribute_contained = attribute.get("contained", None)

        if attribute_contained:
            return attribute_contained
        if attribute_name in self.ui_attributes:
            return self.ui_attributes[attribute_name].is_contained
        if attribute_type in PRIMITIVES:
            return DEFAULT_PRIMITIVE_CONTAINED
        else:
            return DEFAULT_COMPLEX_CONTAINED


class DefaultUIRecipe(UIRecipe):
    def __init__(self):
        super().__init__("Default")
