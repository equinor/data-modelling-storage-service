import json
from typing import Dict, List

from behave import given
import yaml
from storage.internal.data_source_repository import get_data_source
from utils.logging import logger
from utils.package_import import import_package

from domain_classes.dto import DTO
from config import Config


@given("data modelling tool templates are imported")
def step_impl(context):
    for folder in Config.SYSTEM_FOLDERS:
        logger.setLevel("ERROR")
        import_package(f"{Config.APPLICATION_HOME}/system/{folder}", is_root=True, data_source="system")
        logger.setLevel("INFO")


@given('there exist document with id "{uid}" in data source "{data_source_id}"')
def step_impl_2(context, uid: str, data_source_id: str):
    document: DTO = DTO(uid=uid, data=json.loads(context.text))
    document_repository = get_data_source(data_source_id)
    document_repository.add(document)


def store_document_in_data_source(uid: str, data_source_id: str, document: Dict):
    document: DTO = DTO(uid=uid, data=document)
    document_repository = get_data_source(data_source_id)
    document_repository.add(document)


@given('Add to data source "{data_source_id}"')
def create_packages_and_blueprints(context, data_source_id: str):
    yaml_content: Dict = yaml.safe_load(context.text)
    package_names: List[str] = list(yaml_content["RootPackages"].keys())

    # generate package and blueprint documents and store them in data source
    for package_name in package_names:
        package_blueprints: Dict = yaml_content["RootPackages"][f"{package_name}"]["content"]
        package_content: List[Dict] = generate_package_content(package_name, package_blueprints, data_source_id)
        package_document: Dict = generate_root_package_document(package_name, package_content)

        # store package document in data source
        package_uid = yaml_content["RootPackages"][f"{package_name}"]["id"]
        store_document_in_data_source(package_uid, data_source_id, package_document)

        # store blueprint document(s) in data source
        for blueprint_name in list(package_blueprints.keys()):
            blueprint: Dict = package_blueprints[f"{blueprint_name}"]
            blueprint_document: Dict = generate_blueprint_document(blueprint, blueprint_name)
            blueprint_uid = blueprint["id"]
            store_document_in_data_source(blueprint_uid, data_source_id, blueprint_document)


def generate_blueprint_document(blueprint: Dict, blueprint_name: str):
    attributes_list: List[Dict] = []
    append_default_attributes(attributes_list)  # default attributes = type, description and name

    for attribute_name in list(blueprint["attributes"].keys()):
        attribute = blueprint["attributes"][f"{attribute_name}"]
        attribute["name"] = attribute_name
        attribute["type"] = "system/SIMOS/BlueprintAttribute"
        attributes_list.append(attribute)

    storage_recipes: List = get_storage_recipes(blueprint)
    blueprint_document = {
        "type": blueprint["type"],
        "name": blueprint_name,
        "description": "",
        "attributes": attributes_list,
        "storageRecipes": storage_recipes,
        "uiRecipes": [],
    }
    return blueprint_document


def get_storage_recipes(blueprint: Dict):
    if "storageRecipes" in blueprint:
        storage_recipes: List[Dict] = []
        for storage_recipe_name in list(blueprint["storageRecipes"].keys()):
            recipe: Dict = blueprint["storageRecipes"][f"{storage_recipe_name}"]
            recipie_attributes_list: list = []
            for attribute_name in recipe["attributes"]:
                pass
                recipe_attribute: Dict = recipe["attributes"][f"{attribute_name}"]
                recipe_attribute["name"] = attribute_name
                recipie_attributes_list.append(recipe_attribute)
            recipe["attributes"] = recipie_attributes_list
            recipe["name"] = storage_recipe_name
            recipe["description"] = ""
            storage_recipes.append(recipe)
    else:
        storage_recipes: List = []
    return storage_recipes


def append_default_attributes(attributes_list: List[Dict]):
    attributes_list.append({"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"})
    attributes_list.append(
        {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "optional": "true",
            "default": "",
            "name": "description",
        }
    )
    attributes_list.append({"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"})


def generate_package_content(package_name: str, package_blueprints: List[Dict], data_source_id: str):
    package_content: List[Dict] = []
    for blueprint_name in list(package_blueprints.keys()):
        blueprint = package_blueprints[f"{blueprint_name}"]
        package_blueprint_info = {
            "_id": blueprint["id"],
            "name": blueprint_name,
            "type": f"{data_source_id}/{package_name}/{blueprint_name}",
        }
        package_content.append(package_blueprint_info)
    return package_content


def generate_root_package_document(package_name: str, package_content: List[Dict], storage_recipes: List = []):
    package: Dict = {
        "name": package_name,
        "description": "",
        "type": "system/SIMOS/Package",
        "content": package_content,
        "isRoot": "true",
        "storageRecipes": storage_recipes,
        "uiRecipes": [],
    }
    return package
