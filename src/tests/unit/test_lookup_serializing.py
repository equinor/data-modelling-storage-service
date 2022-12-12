import unittest

from domain_classes.lookup import Lookup

lookup_dict = {
    "_id": "DMSS",
    "ui_recipes": {
        "dmss://system/SIMOS/Blueprint": [
            {
                "name": "Yaml",
                "type": "dmss://system/SIMOS/UiRecipe",
                "attributes": [],
                "description": "",
                "plugin": "yaml-view",
                "category": "",
                "roles": None,
                "config": None,
                "label": "",
            },
            {
                "name": "Edit",
                "type": "dmss://system/SIMOS/UiRecipe",
                "attributes": [],
                "description": "Default blueprint edit",
                "plugin": "edit-blueprint",
                "category": "",
                "roles": None,
                "config": None,
                "label": "",
            },
            {
                "name": "Diagram",
                "type": "dmss://system/SIMOS/UiRecipe",
                "attributes": [],
                "description": "",
                "plugin": "mermaid",
                "category": "",
                "roles": None,
                "config": None,
                "label": "",
            },
        ],
        "dmss://system/SIMOS/Entity": [
            {
                "name": "DEFAULT_CREATE",
                "type": "dmss://system/SIMOS/UiRecipe",
                "attributes": [
                    {
                        "name": "type",
                        "contained": True,
                        "field": "blueprint",
                        "array_field": None,
                        "collapsible": None,
                        "ui_recipe": None,
                        "mapping": None,
                    }
                ],
                "description": "",
                "plugin": "Default",
                "category": "",
                "roles": None,
                "config": None,
                "label": "",
            }
        ],
    },
    "storage_recipes": {
        "dmss://system/SIMOS/Blueprint": [
            {
                "name": "DefaultStorageRecipe",
                "type": "dmss://system/SIMOS/StorageRecipe",
                "attributes": {
                    "attributes": {
                        "name": "attributes",
                        "type": "dmss://system/SIMOS/StorageAttribute",
                        "contained": True,
                        "storage_affinity": "default",
                        "label": "",
                        "description": "",
                    },
                    "storageRecipes": {
                        "name": "storageRecipes",
                        "type": "dmss://system/SIMOS/StorageAttribute",
                        "contained": True,
                        "storage_affinity": "default",
                        "label": "",
                        "description": "",
                    },
                    "uiRecipes": {
                        "name": "uiRecipes",
                        "type": "dmss://system/SIMOS/StorageAttribute",
                        "contained": True,
                        "storage_affinity": "default",
                        "label": "",
                        "description": "",
                    },
                },
                "storage_affinity": "default",
                "description": "",
            }
        ],
        "dmss://system/SIMOS/Entity": [],
    },
}


class LookupTestCase(unittest.TestCase):
    def test_lookup(self):
        lookup = Lookup(**lookup_dict)

        assert len(lookup.ui_recipes["dmss://system/SIMOS/Entity"]) == 1
