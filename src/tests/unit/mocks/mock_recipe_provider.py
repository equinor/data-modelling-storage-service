import json
from collections import defaultdict

from domain_classes.storage_recipe import StorageAttribute, StorageRecipe
from enums import StorageDataTypes


class MockStorageRecipeProvider:
    def __init__(self, path_to_mock_storage_recipes: str):
        self.path_to_mock_storage_recipes = path_to_mock_storage_recipes

    def provider(self, type: str, context: str) -> list[StorageRecipe]:
        all_storage_recipes: dict = defaultdict(list)
        with open(self.path_to_mock_storage_recipes) as f:
            all_storage_recipes.update(json.load(f))
        return [
            StorageRecipe(
                name=sr.get("name"),
                storage_affinity=StorageDataTypes(sr.get("storageAffinity", "default")),
                attributes={
                    a["name"]: StorageAttribute(
                        name=a["name"], contained=a["contained"], storage_affinity=a.get("storageAffinity", "default")
                    )
                    for a in sr.get("attributes", [])
                },
            )
            for sr in all_storage_recipes[type]
        ]
