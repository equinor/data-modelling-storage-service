import unittest

from common.utils.replace_reference_with_alias import (
    replace_absolute_references_in_entity_with_alias,
)
from domain_classes.dependency import Dependency

example_entity: dict = {
    "_id": "25cdcef6-ee7c-4377-9487-2f4b8496e7c9",
    "name": "Car",
    "type": "dmss://system/SIMOS/Blueprint",
    "extends": ["dmss://system/SIMOS/NamedEntity", "dmss://DemoApplicationDataSource/models/CarPackage/Vehicle"],
    "description": "",
    "attributes": [
        {
            "name": "color",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "dmss://system/SIMOS/string",
            "blob": {
                "name": "color_profile.txt",
                "type": "dmss://system/SIMOS/Blob",
                "_blob_id": "04cf2783-6118-4bfd-a427-9485b00fa9da",
            },
        },
        {
            "name": "wheels",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "dmss://DemoApplicationDataSource/models/CarPackage/Wheel",
            "dimensions": "*",
        },
    ],
}


entity_with_aliases: dict = {
    "_id": "25cdcef6-ee7c-4377-9487-2f4b8496e7c9",
    "name": "Car",
    "type": "CORE:Blueprint",
    "extends": ["CORE:NamedEntity", "CAR_PACKAGE:Vehicle"],
    "description": "",
    "attributes": [
        {
            "name": "color",
            "type": "CORE:BlueprintAttribute",
            "attributeType": "CORE:string",
            "blob": {
                "name": "color_profile.txt",
                "type": "CORE:Blob",
                "_blob_id": "04cf2783-6118-4bfd-a427-9485b00fa9da",
            },
        },
        {"name": "wheels", "type": "CORE:BlueprintAttribute", "attributeType": "CAR_PACKAGE:Wheel", "dimensions": "*"},
    ],
}


class ReplaceWithAliasTest(unittest.TestCase):
    def test_replace_absolute_references_with_alias(self):

        core_dependency = {"alias": "CORE", "address": "system/SIMOS", "version": "0.0.1", "protocol": "dmss"}
        car_package_dependency = {
            "alias": "CAR_PACKAGE",
            "address": "DemoApplicationDataSource/models/CarPackage",
            "version": "0.0.1",
            "protocol": "dmss",
        }
        dependencies: list[Dependency] = [Dependency(**core_dependency), Dependency(**car_package_dependency)]

        replace_absolute_references_in_entity_with_alias(entity=example_entity, dependencies=dependencies)
        assert example_entity == entity_with_aliases
