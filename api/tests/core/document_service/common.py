from api.classes.blueprint import Blueprint
from api.classes.dto import DTO
from api.core.storage.repositories.file import TemplateRepositoryFromFile
from api.utils.helper_functions import schemas_location

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

file_repository_test = TemplateRepositoryFromFile(schemas_location())


class BlueprintProvider:
    @staticmethod
    def get_blueprint(type: str):
        if type == "blueprint_1":
            return Blueprint(DTO(blueprint_1))
        if type == "blueprint_2":
            return Blueprint(DTO(blueprint_2))
        if type == "uncontained_blueprint":
            return Blueprint(DTO(uncontained_blueprint))
        if type == "blueprint_with_second_level_nested_uncontained_attribute":
            return Blueprint(DTO(blueprint_with_second_level_nested_uncontained_attribute))
        if type == "blueprint_with_optional_attr":
            return Blueprint(DTO(blueprint_with_optional_attr))
        if type == "blueprint_with_nested_optional_attr":
            return Blueprint(DTO(blueprint_with_nested_optional_attr))
        else:
            return Blueprint(DTO(file_repository_test.get(type)))


blueprint_provider = BlueprintProvider()
