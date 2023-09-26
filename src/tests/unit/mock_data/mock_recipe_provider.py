import json
from collections import defaultdict

from domain_classes.storage_recipe import StorageAttribute, StorageRecipe
from enums import StorageDataTypes


def mock_storage_recipe_provider(type: str, context: str) -> list[StorageRecipe]:
    all_storage_recipes = defaultdict(list)
    with open("src/tests/unit/mock_data/mock_storage_recipes/mock_storage_recipes.json") as f:
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
