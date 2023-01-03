import unittest

from common.utils.replace_reference_with_alias import (
    replace_absolute_references_in_entity_with_alias,
    replace_reference_with_alias_if_possible,
)
from domain_classes.dependency import Dependency

example_entity: dict = {
    "_id": "25cdcef6-ee7c-4377-9487-2f4b8496e7c9",
    "name": "Car",
    "_blueprintPath_": "dmss://system/SIMOS/Blueprint",
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
        {
            "name": "wheelPressures",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "dmss://DemoApplicationDataSource/models/CarPackage/Wheel/WheelProperties/Pressures",
            "dimensions": "*",
        },
        {
            "name": "owner",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "dmss://DemoApplicationDataSource/models/Person",
        },
    ],
}


entity_with_aliases: dict = {
    "_id": "25cdcef6-ee7c-4377-9487-2f4b8496e7c9",
    "name": "Car",
    "_blueprintPath_": "CORE:Blueprint",
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
        {
            "name": "wheelPressures",
            "type": "CORE:BlueprintAttribute",
            "attributeType": "WHEEL:WheelProperties/Pressures",
            "dimensions": "*",
        },
        {
            "name": "owner",
            "type": "CORE:BlueprintAttribute",
            "attributeType": "dmss://DemoApplicationDataSource/models/Person",
        },
    ],
}


class ReplaceWithAliasTest(unittest.TestCase):
    def test_replace_ref_with_alias(self):
        car_package_dependency = {
            "alias": "CAR_PACKAGE",
            "address": "DemoApplicationDataSource/models/CarPackage",
            "version": "0.0.1",
            "protocol": "dmss",
        }
        wheel_package_dependency = {
            "alias": "WHEEL",
            "address": "DemoApplicationDataSource/models/CarPackage/Wheel",
            "version": "0.0.1",
            "protocol": "dmss",
        }
        dependencies: list[Dependency] = [Dependency(**car_package_dependency), Dependency(**wheel_package_dependency)]
        reference = "dmss://DemoApplicationDataSource/models/CarPackage/Wheel/SubPackage/Pressure"
        alias = replace_reference_with_alias_if_possible(reference=reference, dependencies=dependencies)
        assert alias == "WHEEL:SubPackage/Pressure"

        reference = "dmss://DemoApplicationDataSource/models"
        alias = replace_reference_with_alias_if_possible(reference=reference, dependencies=dependencies)
        assert alias == reference

    def test_replace_absolute_references_in_entity_with_alias(self):

        core_dependency = {"alias": "CORE", "address": "system/SIMOS", "version": "0.0.1", "protocol": "dmss"}
        car_package_dependency = {
            "alias": "CAR_PACKAGE",
            "address": "DemoApplicationDataSource/models/CarPackage",
            "version": "0.0.1",
            "protocol": "dmss",
        }
        wheel_package_dependency = {
            "alias": "WHEEL",
            "address": "DemoApplicationDataSource/models/CarPackage/Wheel",
            "version": "0.0.1",
            "protocol": "dmss",
        }
        dependencies: list[Dependency] = [
            Dependency(**core_dependency),
            Dependency(**car_package_dependency),
            Dependency(**wheel_package_dependency),
        ]
        new_entity_with_alias = replace_absolute_references_in_entity_with_alias(
            entity=example_entity, dependencies=dependencies
        )
        assert new_entity_with_alias == entity_with_aliases
