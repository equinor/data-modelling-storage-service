from collections import defaultdict

from domain_classes.storage_recipe import StorageAttribute, StorageRecipe
from enums import SIMOS, StorageDataTypes
from services.document_service import DocumentService


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
    "extends": [SIMOS.NAMED_ENTITY.value],
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

fuel_pump = {
    "type": "system/SIMOS/Blueprint",
    "name": "FuelPumpTest",
    "description": "This describes a fuel pump",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "description",
            "default": "A standard fuel pump",
        },
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
    ],
}

engine = {
    "type": "system/SIMOS/Blueprint",
    "name": "EngineTest",
    "description": "This describes an engine",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "description",
        },
        {
            "attributeType": "integer",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "power",
            "default": 120,
        },
        {
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "test_data/complex/FuelPumpTest",
            "name": "fuelPump",
            "default": {
                "description": "A standard fuel pump",
                "name": "fuelPump",
                "type": "test_data/complex/FuelPumpTest",
            },
        },
    ],
}

car = {
    "type": "system/SIMOS/Blueprint",
    "name": "CarTest",
    "attributes": [
        {
            "name": "name",
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "default": "CarTest",
        },
        {
            "name": "type",
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "default": "test_data/complex/CarTest",
        },
        {
            "name": "plateNumber",
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
        },
        {
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "wheel",
            "attributeType": "test_data/complex/WheelTest",
        },
        {
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "wheels",
            "attributeType": "test_data/complex/WheelTest",
            "dimensions": "*",
        },
        {
            "name": "seats",
            "attributeType": "integer",
            "type": "system/SIMOS/BlueprintAttribute",
            "default": 2,
        },
        {
            "name": "is_sedan",
            "attributeType": "boolean",
            "type": "system/SIMOS/BlueprintAttribute",
            "default": True,
        },
        {
            "name": "floatValues",
            "attributeType": "number",
            "type": "system/SIMOS/BlueprintAttribute",
            "dimensions": "*",
            "default": [2.1, 3.1, 4.2],
        },
        {
            "name": "intValues",
            "attributeType": "integer",
            "type": "system/SIMOS/BlueprintAttribute",
            "dimensions": "*",
            "default": [1, 5, 4, 2],
        },
        {
            "name": "boolValues",
            "attributeType": "boolean",
            "type": "system/SIMOS/BlueprintAttribute",
            "dimensions": "*",
            "default": [True, False, True],
        },
        {
            "name": "stringValues",
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "dimensions": "*",
            "default": ["one", "two", "three"],
        },
        {
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "engine",
            "attributeType": "test_data/complex/EngineTest",
        },
        {
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "engine2",
            "optional": True,
            "attributeType": "test_data/complex/EngineTest",
        },
        {
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "engine3",
            "optional": True,
            "attributeType": "test_data/complex/EngineTest",
            "default": {
                "name": "default engine",
                "fuelPump": {
                    "name": "fuelPump",
                    "description": "A standard fuel pump",
                    "type": "test_data/complex/FuelPumpTest",
                },
                "power": 9,
                "type": "test_data/complex/EngineTest",
            },
        },
    ],
}
wheel = {
    "name": "WheelTest",
    "type": "system/SIMOS/Blueprint",
    "attributes": [
        {
            "name": "name",
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "default": "Wheel",
        },
        {"name": "type", "attributeType": "string", "type": "system/SIMOS/BlueprintAttribute"},
        {
            "name": "power",
            "attributeType": "number",
            "type": "system/SIMOS/BlueprintAttribute",
            "default": 0.0,
        },
    ],
}

car_rental = {
    "name": "CarRental",
    "type": "system/SIMOS/Blueprint",
    "attributes": [
        {"name": "name", "attributeType": "string", "type": "system/SIMOS/BlueprintAttribute"},
        {"name": "type", "attributeType": "string", "type": "system/SIMOS/BlueprintAttribute"},
        {
            "name": "cars",
            "dimensions": "*",
            "attributeType": "test_data/complex/RentalCar",
            "type": "system/SIMOS/BlueprintAttribute",
        },
        {
            "name": "customers",
            "dimensions": "*",
            "attributeType": "test_data/complex/Customer",
            "type": "system/SIMOS/BlueprintAttribute",
        },
    ],
}

car_rental_car = {
    "type": "system/SIMOS/Blueprint",
    "name": "RentalCar",
    "attributes": [
        {
            "name": "name",
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "default": "RentalCar",
        },
        {
            "name": "type",
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "default": "test_data/complex/RentalCar",
        },
        {
            "name": "plateNumber",
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
        },
        {
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "engine",
            "attributeType": "test_data/complex/EngineTest",
            "optional": True,
        },
    ],
}

car_rental_customer = {
    "name": "Customer",
    "type": "system/SIMOS/Blueprint",
    "attributes": [
        {"name": "name", "attributeType": "string", "type": "system/SIMOS/BlueprintAttribute"},
        {
            "name": "car",
            "attributeType": "test_data/complex/RentalCar",
            "type": "system/SIMOS/BlueprintAttribute",
            "contained": False,
        },
    ],
}

parent = {
    "type": "dmss://system/SIMOS/Blueprint",
    "name": "Parent",
    "description": "",
    "extends": ["dmss://system/SIMOS/NamedEntity"],
    "attributes": [
        {"name": "SomeChild", "attributeType": "BaseChild", "type": "dmss://system/SIMOS/BlueprintAttribute"}
    ],
}

base_child = {
    "type": "dmss://system/SIMOS/Blueprint",
    "name": "BaseChild",
    "description": "",
    "extends": ["dmss://system/SIMOS/NamedEntity"],
    "attributes": [{"name": "AValue", "attributeType": "integer", "type": "dmss://system/SIMOS/BlueprintAttribute"}],
}

special_child = {
    "type": "dmss://system/SIMOS/Blueprint",
    "name": "SpecialChild",
    "description": "",
    "extends": ["BaseChild"],
    "attributes": [
        {"name": "AnExtraValue", "attributeType": "string", "type": "dmss://system/SIMOS/BlueprintAttribute"}
    ],
}

file_repository_test = LocalFileRepository()


class BlueprintProvider:
    @staticmethod
    def get_blueprint(type: str):
        if type == "all_contained_cases_blueprint":
            return Blueprint(all_contained_cases_blueprint, type)
        if type == "basic_blueprint":
            return Blueprint(basic_blueprint, type)
        if type == "blueprint_with_second_level_reference":
            return Blueprint(blueprint_with_second_level_reference, type)
        if type == "two_contained_deep_attributes":
            return Blueprint(two_contained_deep_attributes, type)
        if type == "ExtendedBlueprint":
            return Blueprint(extended_blueprint, type)
        if type == "SecondLevelExtendedBlueprint":
            return Blueprint(second_level_extended_blueprint, type)
        if type == "uncontained_blueprint":
            return Blueprint(uncontained_blueprint, type)
        if type == "uncontained_list_blueprint":
            return Blueprint(uncontained_list_blueprint, type)
        if type == "blueprint_with_second_level_nested_uncontained_attribute":
            return Blueprint(blueprint_with_second_level_nested_uncontained_attribute, type)
        if type == "blueprint_with_optional_attr":
            return Blueprint(blueprint_with_optional_attr, type)
        if type == "blueprint_with_nested_optional_attr":
            return Blueprint(blueprint_with_nested_optional_attr, type)
        if type == "blob":
            return Blueprint(blueprint_with_storageAffinity_in_root, type)
        if type == "blobContainer":
            return Blueprint(blobContainer, type)
        if type == "blueprint_with_blob":
            return Blueprint(blueprint_with_blob, type)
        if type == "test_data/complex/FuelPumpTest":
            return Blueprint(fuel_pump, type)
        if type == "test_data/complex/EngineTest":
            return Blueprint(engine, type)
        if type == "test_data/complex/CarTest":
            return Blueprint(car, type)
        if type == "test_data/complex/WheelTest":
            return Blueprint(wheel, type)
        if type == "test_data/complex/CarRental":
            return Blueprint(car_rental, type)
        if type == "test_data/complex/RentalCar":
            return Blueprint(car_rental_car, type)
        if type == "test_data/complex/Customer":
            return Blueprint(car_rental_customer, type)
        if type == "Parent":
            return Blueprint(parent, type)
        if type == "BaseChild":
            return Blueprint(base_child, type)
        if type == "SpecialChild":
            return Blueprint(special_child, type)
        else:
            return Blueprint(file_repository_test.get(type), type)


blueprint_provider = BlueprintProvider()

all_storage_recipes = defaultdict(list)
all_storage_recipes.update(
    {
        "all_contained_cases_blueprint": [
            {
                "type": "dmss://system/SIMOS/StorageRecipe",
                "name": "DefaultStorageRecipe",
                "description": "",
                "attributes": [
                    {"name": "reference", "type": "dmss://system/SIMOS/Entity", "contained": False},
                    {"name": "references", "type": "dmss://system/SIMOS/Entity", "contained": False},
                ],
            }
        ],
        "uncontained_blueprint": [
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
        ],
        "ExtendedBlueprint": [
            {
                "name": "default",
                "type": "dmss://system/SIMOS/StorageRecipe",
                "description": "",
                "storageAffinity": "blob",
                "attributes": [],
            }
        ],
        # "uncontained_blueprint": uncontained_blueprint,
        "blob": [
            {
                "name": "default",
                "type": "dmss://system/SIMOS/StorageRecipe",
                "description": "",
                "storageAffinity": "blob",
                "attributes": [],
            }
        ],
        "blobContainer": [
            {
                "name": "default",
                "type": "dmss://system/SIMOS/StorageRecipe",
                "description": "",
                "attributes": [{"name": "blob", "type": "does_this_matter?", "contained": False}],
            }
        ],
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


def get_mock_document_service(
    repository_provider=None,
    blueprint_provider=blueprint_provider,
    recipe_provider=mock_storage_recipe_provider,
    user=None,
    context=None,
):
    return DocumentService(
        blueprint_provider=blueprint_provider,
        recipe_provider=recipe_provider,
        repository_provider=repository_provider,
        user=user,
        context=context,
    )
