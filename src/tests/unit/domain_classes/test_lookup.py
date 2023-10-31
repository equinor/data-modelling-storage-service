import unittest

from domain_classes.lookup import Lookup


class ExtendRecipeLinksTestCase(unittest.TestCase):
    def test_get_recipes_not_extended(self):
        lookup = Lookup(
            **{
                "ui_recipes": {
                    "_default_": [
                        {"name": "Yaml", "type": "dmss://system/SIMOS/UiRecipe"},
                        {"name": "Edit", "type": "dmss://system/SIMOS/UiRecipe"},
                    ],
                    "dmss://system/SIMOS/Entity": [{"name": "DEFAULT_CREATE", "type": "dmss://system/SIMOS/UiRecipe"}],
                    "dmss://system/SIMOS/blob_types/PDF": [{"name": "PDFView", "type": "dmss://system/SIMOS/UiRecipe"}],
                }
            }
        )

        lookup.realize_extends()

        assert len(lookup.ui_recipes["dmss://system/SIMOS/blob_types/PDF"]) == 1

    def test_get_recipes_2_levels_extended(self):
        lookup = Lookup(
            **{
                "ui_recipes": {
                    "some_other_base": [{"name": "FROM-BASE", "type": "dmss://system/SIMOS/UiRecipe"}],
                    "_default_": [
                        {"name": "Yaml", "type": "dmss://system/SIMOS/UiRecipe"},
                        {"name": "Edit", "type": "dmss://system/SIMOS/UiRecipe"},
                    ],
                    "dmss://system/SIMOS/Entity": [{"name": "DEFAULT_CREATE", "type": "dmss://system/SIMOS/UiRecipe"}],
                    "dmss://system/SIMOS/blob_types/PDF": [{"name": "PDFView", "type": "dmss://system/SIMOS/UiRecipe"}],
                }
            }
        )

        lookup.extends = {
            "dmss://system/SIMOS/blob_types/PDF": [
                "dmss://system/SIMOS/Entity",
                "_default_",
            ],
            "dmss://system/SIMOS/Entity": ["some_other_base"],
        }

        lookup.realize_extends()

        assert len(lookup.ui_recipes["dmss://system/SIMOS/Entity"]) == 2
        assert len(lookup.ui_recipes["dmss://system/SIMOS/blob_types/PDF"]) == 5

    def test_get_storage_recipes_2_levels_extended(self):
        lookup = Lookup(
            **{
                "storage_recipes": {
                    "some_other_base": [{"name": "FROM-BASE", "type": "dmss://system/SIMOS/StorageRecipe"}],
                    "_default_": [
                        {"name": "Yaml", "type": "dmss://system/SIMOS/StorageRecipe"},
                        {"name": "Edit", "type": "dmss://system/SIMOS/StorageRecipe"},
                    ],
                    "dmss://system/SIMOS/Entity": [
                        {
                            "name": "DEFAULT_CREATE",
                            "type": "dmss://system/SIMOS/StorageRecipe",
                        }
                    ],
                    "dmss://system/SIMOS/blob_types/PDF": [
                        {"name": "PDFView", "type": "dmss://system/SIMOS/StorageRecipe"}
                    ],
                }
            }
        )

        lookup.extends = {
            "dmss://system/SIMOS/blob_types/PDF": [
                "dmss://system/SIMOS/Entity",
                "_default_",
            ],
            "dmss://system/SIMOS/Entity": ["some_other_base"],
        }

        lookup.realize_extends()

        assert len(lookup.storage_recipes["dmss://system/SIMOS/Entity"]) == 2
        assert len(lookup.storage_recipes["dmss://system/SIMOS/blob_types/PDF"]) == 5
