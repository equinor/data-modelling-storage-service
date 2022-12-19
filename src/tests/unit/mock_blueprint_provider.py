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
from storage.repositories.file import LocalFileRepository

all_contained_cases_blueprint = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "Blueprint 1",
    "description": "First blueprint",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {"attributeType": "basic_blueprint", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "nested"},
        {"attributeType": "basic_blueprint", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "reference"},
        {
            "attributeType": "basic_blueprint",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "references",
            "dimensions": "*",
        },
    ],
}

blueprint_with_second_level_reference = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "Blueprint with second level reference",
    "description": "Blueprint with second level reference",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {
            "attributeType": "all_contained_cases_blueprint",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "contained_with_child_references",
        },
    ],
}

two_contained_deep_attributes = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "two_contained_deep_attributes",
    "description": "Two contained deeply nested attributes",
    "attributes": [
        {
            "attributeType": "all_contained_cases_blueprint",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "a",
        },
        {
            "attributeType": "all_contained_cases_blueprint",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "b",
        },
    ],
}

basic_blueprint = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "Blueprint 2",
    "description": "Second blueprint",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [],
    "storageRecipes": [],
    "uiRecipes": [{"name": "default", "description": "", "plugin": "edit1"}],
}

extended_blueprint = {
    "type": SIMOS.BLUEPRINT.value,
    "extends": ["basic_blueprint"],
    "name": "ExtendedBlueprint",
    "description": "This Blueprint extends blueprint 2",
    "attributes": [{"attributeType": "string", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "another_value"}],
    "storageRecipes": [
        {
            "name": "default",
            "type": "dmss://system/SIMOS/StorageRecipe",
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
    "type": SIMOS.BLUEPRINT.value,
    "extends": ["ExtendedBlueprint"],
    "name": "SecondLevelExtendedBlueprint",
    "description": "This Blueprint extends 'ExtendedBlueprint'",
    "attributes": [{"attributeType": "string", "type": SIMOS.BLUEPRINT_ATTRIBUTE.value, "name": "a_third_value"}],
    "storageRecipes": [],
    "uiRecipes": [],
}

uncontained_blueprint = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "uncontained_blueprint",
    "description": "uncontained_blueprint",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {
            "attributeType": "basic_blueprint",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "uncontained_in_every_way",
            "contained": False,
        },
    ],
}

uncontained_list_blueprint = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "uncontained_list_blueprint",
    "description": "uncontained_list_blueprint",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {
            "attributeType": "basic_blueprint",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "uncontained_in_every_way",
            "contained": False,
            "dimensions": "*",
        },
    ],
}

blueprint_with_second_level_nested_uncontained_attribute = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "blueprint_with_second_level_nested_uncontained_attribute",
    "description": "",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {
            "attributeType": "uncontained_blueprint",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "i_have_a_uncontained_attribute",
        },
    ],
}

blueprint_with_optional_attr = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "Blueprint_with_optional_attr",
    "description": "",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {
            "attributeType": "basic_blueprint",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "im_optional",
            "optional": True,
            "contained": True,
        },
    ],
}

blueprint_with_blob = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "Blueprint_with_blob",
    "description": "",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {
            "attributeType": SIMOS.BLOB.value,
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "blob",
        },
    ],
}

blueprint_with_nested_optional_attr = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "blueprint_with_nested_optional_attr",
    "description": "",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {
            "attributeType": "blueprint_with_optional_attr",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "nested_with_optional",
        },
    ],
}

blueprint_with_storageAffinity_in_root = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "blob",
    "description": "Test for a blueprint with storageAffinity in storageRecipe",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {
            "attributeType": "string",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "someData",
            "default": "",
        },
    ],
    "storageRecipes": [
        {
            "name": "default",
            "type": "dmss://system/SIMOS/StorageRecipe",
            "description": "",
            "storageAffinity": "blob",
            "attributes": [],
        }
    ],
}

blobContainer = {
    "type": SIMOS.BLUEPRINT.value,
    "name": "blobContainer",
    "description": "A basic blueprint that has a non-storageContained blob, none specified storageAffinity ",
    "extends": [SIMOS.NAMED_ENTITY.value],
    "attributes": [
        {
            "attributeType": "blob",
            "type": SIMOS.BLUEPRINT_ATTRIBUTE.value,
            "name": "blob",
        },
    ],
    "storageRecipes": [
        {
            "name": "default",
            "type": "dmss://system/SIMOS/StorageRecipe",
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
            return Blueprint(all_contained_cases_blueprint)
        if type == "basic_blueprint":
            return Blueprint(basic_blueprint)
        if type == "blueprint_with_second_level_reference":
            return Blueprint(blueprint_with_second_level_reference)
        if type == "two_contained_deep_attributes":
            return Blueprint(two_contained_deep_attributes)
        if type == "ExtendedBlueprint":
            return Blueprint(extended_blueprint)
        if type == "SecondLevelExtendedBlueprint":
            return Blueprint(second_level_extended_blueprint)
        if type == "uncontained_blueprint":
            return Blueprint(uncontained_blueprint)
        if type == "uncontained_list_blueprint":
            return Blueprint(uncontained_list_blueprint)
        if type == "blueprint_with_second_level_nested_uncontained_attribute":
            return Blueprint(blueprint_with_second_level_nested_uncontained_attribute)
        if type == "blueprint_with_optional_attr":
            return Blueprint(blueprint_with_optional_attr)
        if type == "blueprint_with_nested_optional_attr":
            return Blueprint(blueprint_with_nested_optional_attr)
        if type == "blob":
            return Blueprint(blueprint_with_storageAffinity_in_root)
        if type == "blobContainer":
            return Blueprint(blobContainer)
        if type == "blueprint_with_blob":
            return Blueprint(blueprint_with_blob)
        else:
            return Blueprint(file_repository_test.get(type))


blueprint_provider = BlueprintProvider()
