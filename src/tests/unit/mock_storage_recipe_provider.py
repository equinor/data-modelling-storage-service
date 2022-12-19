from collections import defaultdict

from domain_classes.storage_recipe import StorageAttribute, StorageRecipe
from enums import StorageDataTypes

all_contained_cases_blueprint = [
    {
        "type": "dmss://system/SIMOS/StorageRecipe",
        "name": "DefaultStorageRecipe",
        "description": "",
        "attributes": [
            {"name": "reference", "type": "dmss://system/SIMOS/Entity", "contained": False},
            {"name": "references", "type": "dmss://system/SIMOS/Entity", "contained": False},
        ],
    }
]

extended_blueprint = [
    {
        "name": "default",
        "type": "dmss://system/SIMOS/StorageRecipe",
        "description": "",
        "storageAffinity": "blob",
        "attributes": [],
    }
]

package_blueprint = [
    {
        "type": "dmss://system/SIMOS/StorageRecipe",
        "name": "DefaultStorageRecipe",
        "description": "",
        "attributes": [{"name": "content", "type": "object", "contained": False}],
    }
]

uncontained_blueprint = [
    {
        "type": "dmss://system/SIMOS/StorageRecipe",
        "name": "DefaultStorageRecipe",
        "description": "",
        "attributes": [
            {
                "name": "uncontained_in_every_way",
                "type": "does_this_matter?",
                "contained": False,
                "storageAffinity": "blob",
            }
        ],
    }
]

blueprint_with_storageAffinity_in_root = [
    {
        "name": "default",
        "type": "dmss://system/SIMOS/StorageRecipe",
        "description": "",
        "storageAffinity": "blob",
        "attributes": [],
    }
]

blob_container = [
    {
        "name": "default",
        "type": "dmss://system/SIMOS/StorageRecipe",
        "description": "",
        "attributes": [{"name": "blob", "type": "does_this_matter?", "contained": False}],
    }
]

all_storage_recipes = defaultdict(list)
all_storage_recipes.update(
    {
        "all_contained_cases_blueprint": all_contained_cases_blueprint,
        "ExtendedBlueprint": extended_blueprint,
        "uncontained_blueprint": uncontained_blueprint,
        "blob": blueprint_with_storageAffinity_in_root,
        "blobContainer": blob_container,
    }
)


def mock_storage_recipe_provider(type: str, context: str) -> list[StorageRecipe]:
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
