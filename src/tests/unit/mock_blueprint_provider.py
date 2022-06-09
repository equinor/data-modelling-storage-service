# https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys
from enums import SIMOS


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

all_contained_cases_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint 1",
    "description": "First blueprint",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {"attributeType": "basic_blueprint", "type": "system/SIMOS/BlueprintAttribute", "name": "nested"},
        {"attributeType": "basic_blueprint", "type": "system/SIMOS/BlueprintAttribute", "name": "reference"},
        {
            "attributeType": "basic_blueprint",
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
}

blueprint_with_second_level_reference = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint with second level reference",
    "description": "Blueprint with second level reference",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {
            "attributeType": "all_contained_cases_blueprint",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "contained_with_child_references",
        },
    ],
}

two_contained_deep_attributes = {
    "type": "system/SIMOS/Blueprint",
    "name": "two_contained_deep_attributes",
    "description": "Two contained deeply nested attributes",
    "attributes": [
        {"attributeType": "all_contained_cases_blueprint", "type": "system/SIMOS/BlueprintAttribute", "name": "a"},
        {"attributeType": "all_contained_cases_blueprint", "type": "system/SIMOS/BlueprintAttribute", "name": "b"},
    ],
}

basic_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint 2",
    "description": "Second blueprint",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [],
    "storageRecipes": [],
    "uiRecipes": [{"name": "default", "description": "", "plugin": "edit1"}],
}

extended_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "extends": ["basic_blueprint"],
    "name": "ExtendedBlueprint",
    "description": "This Blueprint extends blueprint 2",
    "attributes": [{"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "another_value"}],
    "storageRecipes": [
        {
            "name": "default",
            "type": "system/SIMOS/StorageRecipe",
            "description": "",
            "storageAffinity": "blob",
            "attributes": [],
        }
    ],
    "uiRecipes": [
        {"name": "default", "description": "", "plugin": "edit2"},
        {"name": "aSpecialView", "description": "", "plugin": "specialView"},
    ],
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
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {
            "attributeType": "basic_blueprint",
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

uncontained_list_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "uncontained_list_blueprint",
    "description": "uncontained_list_blueprint",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {
            "attributeType": "basic_blueprint",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "uncontained_in_every_way",
            "contained": False,
            "dimensions": "*",
        },
    ],
}

blueprint_with_second_level_nested_uncontained_attribute = {
    "type": "system/SIMOS/Blueprint",
    "name": "blueprint_with_second_level_nested_uncontained_attribute",
    "description": "",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
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
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {
            "attributeType": "basic_blueprint",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "im_optional",
            "optional": True,
            "contained": True,
        },
    ],
}

blueprint_with_blob = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint_with_blob",
    "description": "",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {
            "attributeType": SIMOS.BLOB.value,
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "blob",
        },
    ],
}

blueprint_with_nested_optional_attr = {
    "type": "system/SIMOS/Blueprint",
    "name": "blueprint_with_nested_optional_attr",
    "description": "",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
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
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
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
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {
            "attributeType": "blob",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "blob",
        },
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
        if type == "all_contained_cases_blueprint":
            return Blueprint(DTO(all_contained_cases_blueprint))
        if type == "basic_blueprint":
            return Blueprint(DTO(basic_blueprint))
        if type == "blueprint_with_second_level_reference":
            return Blueprint(DTO(blueprint_with_second_level_reference))
        if type == "two_contained_deep_attributes":
            return Blueprint(DTO(two_contained_deep_attributes))
        if type == "ExtendedBlueprint":
            return Blueprint(DTO(extended_blueprint))
        if type == "SecondLevelExtendedBlueprint":
            return Blueprint(DTO(second_level_extended_blueprint))
        if type == "uncontained_blueprint":
            return Blueprint(DTO(uncontained_blueprint))
        if type == "uncontained_list_blueprint":
            return Blueprint(DTO(uncontained_list_blueprint))
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
        if type == "blueprint_with_blob":
            return Blueprint(DTO(blueprint_with_blob))
        else:
            return Blueprint(DTO(file_repository_test.get(type)))


blueprint_provider = BlueprintProvider()
