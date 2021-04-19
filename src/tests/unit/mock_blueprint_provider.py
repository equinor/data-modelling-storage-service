# https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys
def flatten_dict(dd, separator="_", prefix=""):
    return (
        {
            prefix + separator + k if prefix else k: v
            for kk, vv in dd.items()
            for k, v in flatten_dict(vv, separator, kk).items()
        }
        if isinstance(dd, dict)
        else {prefix: dd}
    )


from domain_classes.blueprint import Blueprint
from domain_classes.dto import DTO
from storage.repositories.file import LocalFileRepository

blueprint_1 = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint 1",
    "description": "First blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {"attributeType": "blueprint_2", "type": "system/SIMOS/BlueprintAttribute", "name": "nested"},
        {"attributeType": "blueprint_2", "type": "system/SIMOS/BlueprintAttribute", "name": "reference"},
        {
            "attributeType": "blueprint_2",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "references",
            "dimensions": "*",
        },
    ],
    "storageRecipes": [
        {
            "type": "system/SIMOS/StorageRecipe",
            "name": "DefaultStorageRecipe",
            "description": "",
            "attributes": [
                {"name": "reference", "type": "system/SIMOS/Entity", "contained": False},
                {"name": "references", "type": "system/SIMOS/Entity", "contained": False},
            ],
        }
    ],
    "uiRecipes": [],
}

blueprint_2 = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint 2",
    "description": "Second blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
    ],
    "storageRecipes": [],
    "uiRecipes": [{"name": "default", "description": "", "plugin": "edit1"}],
}

extended_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "extends": ["blueprint_2"],
    "name": "ExtendedBlueprint",
    "description": "This Blueprint extends blueprint 2",
    "attributes": [{"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "another_value"},],
    "storageRecipes": [
        {
            "name": "default",
            "type": "system/SIMOS/StorageRecipe",
            "description": "",
            "storageAffinity": "blob",
            "attributes": [],
        }
    ],
    "uiRecipes": [{"name": "default", "description": "", "plugin": "edit2"}],
}

second_level_extended_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "extends": ["ExtendedBlueprint"],
    "name": "SecondLevelExtendedBlueprint",
    "description": "This Blueprint extends 'ExtendedBlueprint'",
    "attributes": [{"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "a_third_value"}],
    "storageRecipes": [],
    "uiRecipes": [],
}

uncontained_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "uncontained_blueprint",
    "description": "uncontained_blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {
            "attributeType": "blueprint_2",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "uncontained_in_every_way",
            "contained": False,
        },
    ],
    "storageRecipes": [
        {
            "type": "system/SIMOS/StorageRecipe",
            "name": "DefaultStorageRecipe",
            "description": "",
            "attributes": [
                {
                    "name": "uncontained_in_every_way",
                    "type": "does_this_matter?",
                    "contained": False,
                    "storageTypeAffinity": "blob",
                }
            ],
        }
    ],
}

blueprint_with_second_level_nested_uncontained_attribute = {
    "type": "system/SIMOS/Blueprint",
    "name": "blueprint_with_second_level_nested_uncontained_attribute",
    "description": "",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {
            "attributeType": "uncontained_blueprint",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "i_have_a_uncontained_attribute",
        },
    ],
}

blueprint_with_optional_attr = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint_with_optional_attr",
    "description": "",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {
            "attributeType": "blueprint_2",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "im_optional",
            "optional": True,
            "contained": True,
        },
    ],
}

blueprint_with_nested_optional_attr = {
    "type": "system/SIMOS/Blueprint",
    "name": "blueprint_with_nested_optional_attr",
    "description": "",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {
            "attributeType": "blueprint_with_optional_attr",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "nested_with_optional",
        },
    ],
}

blueprint_with_storageAffinity_in_root = {
    "type": "system/SIMOS/Blueprint",
    "name": "blob",
    "description": "Test for a blueprint with storageAffinity in storageRecipe",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "someData", "default": ""},
    ],
    "storageRecipes": [
        {
            "name": "default",
            "type": "system/SIMOS/StorageRecipe",
            "description": "",
            "storageAffinity": "blob",
            "attributes": [],
        }
    ],
}

blobContainer = {
    "type": "system/SIMOS/Blueprint",
    "name": "blobContainer",
    "description": "A basic blueprint that has a non-storageContained blob, none specified storageAffinity ",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {"attributeType": "blob", "type": "system/SIMOS/BlueprintAttribute", "name": "blob",},
    ],
    "storageRecipes": [
        {
            "name": "default",
            "type": "system/SIMOS/StorageRecipe",
            "description": "",
            "attributes": [{"name": "blob", "type": "does_this_matter?", "contained": False}],
        }
    ],
}

file_repository_test = LocalFileRepository()


class BlueprintProvider:
    @staticmethod
    def get_blueprint(type: str):
        if type == "blueprint_1":
            return Blueprint(DTO(blueprint_1))
        if type == "blueprint_2":
            return Blueprint(DTO(blueprint_2))
        if type == "ExtendedBlueprint":
            return Blueprint(DTO(extended_blueprint))
        if type == "SecondLevelExtendedBlueprint":
            return Blueprint(DTO(second_level_extended_blueprint))
        if type == "uncontained_blueprint":
            return Blueprint(DTO(uncontained_blueprint))
        if type == "blueprint_with_second_level_nested_uncontained_attribute":
            return Blueprint(DTO(blueprint_with_second_level_nested_uncontained_attribute))
        if type == "blueprint_with_optional_attr":
            return Blueprint(DTO(blueprint_with_optional_attr))
        if type == "blueprint_with_nested_optional_attr":
            return Blueprint(DTO(blueprint_with_nested_optional_attr))
        if type == "blob":
            return Blueprint(DTO(blueprint_with_storageAffinity_in_root))
        if type == "blobContainer":
            return Blueprint(DTO(blobContainer))
        else:
            return Blueprint(DTO(file_repository_test.get(type)))


blueprint_provider = BlueprintProvider()
