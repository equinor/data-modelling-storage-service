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



def store_document_in_data_source(uid: str, dataSourceId: str, document: Dict):
    document: DTO = DTO(uid=uid, data=document)
    documentRepository = get_data_source(dataSourceId)
    documentRepository.add(document)


@given('Add to data source "{dataSourceId}"')
def convert_yaml_to_json(context, dataSourceId: str):
    yaml_content_as_dict: dict = yaml.safe_load(context.text)
    packageNames: List[string] = list(yaml_content_as_dict['RootPackages'].keys()) #['TestData', 'TestData2']
    package_blueprint_info: Dict

    # generate package and blueprint documents and store them in data source
    for packageName in packageNames:
        packageBlueprints: List[Dict] = yaml_content_as_dict['RootPackages'][f"{packageName}"]['content']
        packageContent: List[Dict] = generate_package_content(packageName, packageBlueprints, dataSourceId)
        packageDocument: Dict = generate_root_package_document(packageName, packageContent)

        packageUid = yaml_content_as_dict['RootPackages'][f"{packageName}"]['id']
        store_document_in_data_source(packageUid, dataSourceId, packageDocument)
        print("--- PACKAGE DOCUMENT ---")
        print(json.dumps(packageDocument, indent=2))
        print(" ")

        #store blueprint documents in data source
        for blueprintName in list(packageBlueprints.keys()):
            blueprint: Dict = packageBlueprints[f'{blueprintName}']
            blueprintDocument: Dict = generate_blueprint_document(blueprint, blueprintName)
            blueprintUid = blueprint['id']
            store_document_in_data_source(blueprintUid, dataSourceId, blueprintDocument)
            print("--- BLUEPRINT DOCUMNET ---")
            print(json.dumps(blueprintDocument, indent=2))
            print(" ")



def generate_blueprint_document(blueprint: Dict, blueprintName: str, storageRecipes: List = []):
    attributesList: List[Dict] = []
    append_default_attributes(
        attributesList)  # default attributes = attributes that exist for all blueprints: type, description and name

    for attributeName in list(blueprint['attributes'].keys()):
        attribute = blueprint['attributes'][f'{attributeName}']
        attribute['name'] = attributeName
        attribute['type'] = "system/SIMOS/BlueprintAttribute" # is it ok to hardcode this value??
        attributesList.append(attribute)

    blueprint_document = {
        "type": blueprint['type'],
        "name": blueprintName,
        "description": "",
        "attributes" : attributesList,
        "storageRecipes": storageRecipes,
        "uiRecipes": []
    }
    return blueprint_document

def append_default_attributes(attributesList: List[Dict]):
    attributesList.append(
        {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "name"
        }
    )
    attributesList.append({
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "optional": "true",
            "default": "",
            "name": "description"
        })
    attributesList.append({
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "type"
        })


def generate_package_content(packageName: str, packageBlueprints: List[Dict], dataSourceId: str):
    ###### packageBlueprintNames: list[str] = list(packageBlueprints.keys())
    packageContent: List[Dict] = []
    for blueprintName in list(packageBlueprints.keys()):
        blueprint = packageBlueprints[f"{blueprintName}"]
        packageBlueprintInfo = {
            "_id": blueprint['id'],
            "name": blueprintName,
            "type": f"{dataSourceId}/{packageName}/{blueprintName}"
        }
        packageContent.append(packageBlueprintInfo)
    return packageContent

#todo move this func to utils or soemthing
def generate_root_package_document(packageName: str, packageContent: List[Dict], storageRecipes: List = []):
    package: Dict = {
        "name": packageName,
        "description": "",
        "type": "system/SIMOS/Package",
        "content": packageContent,
        "isRoot": "true",
        "storageRecipes": storageRecipes,
        "uiRecipes": []
    }
    return package



@given('there exists a package "{packageName}" with id "{uid}" in data source "{dataSourceId}"')
def create_package(context, packageName: str, dataSourceId: str, uid: str):
    package: Dict[Dict, str, str] = {
        "jsonContent": {
            "name": packageName,
            "description": "Example package description",
            "type": "system/SIMOS/Package",
            "content": [],
            "isRoot": "true",
            "storageRecipes": [],
            "uiRecipes": [],
        },
        "dataSourceId": dataSourceId,
        "packageId": uid,
    }

    context.createdPackages = context.createdPackages + [
        package
    ]  # using an array makes it possible to create several packages in a single scenario.
    document: DTO = DTO(uid=package["packageId"], data=package["jsonContent"])
    document_repository = get_data_source(package["dataSourceId"])
    document_repository.add(document)


# a "bare minimum blueprint" = a blueprint with only required attributes (name and type)
@given('the package "{packageName}" contains a bare minimum blueprint "{blueprintName}" with id "{blueprintId}"')
def append_blueprint_to_package(context, packageName: str, blueprintName: str, blueprintId: str):

    # find the package to add the blueprint to
    chosenPackage: Dict
    createdPackages: [Dict] = context.createdPackages
    for package in createdPackages:
        if package["jsonContent"]["name"] == packageName:
            chosenPackage = package

    blueprint: Dict = {
        "jsonContent": {
            "type": "system/SIMOS/Blueprint",
            "name": blueprintName,
            "description": "",
            "attributes": [
                {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
                {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
            ],
            "storageRecipes": [],
            "uiRecipes": [],
        },
        "blueprintId": blueprintId,
        "dataSourceId": chosenPackage["dataSourceId"],
    }

    # add blueprint to storage
    document: DTO = DTO(uid=blueprint["blueprintId"], data=blueprint["jsonContent"])
    document_repository = get_data_source(
        blueprint["dataSourceId"]
    )  # question: can package and blueprint have different data sources???
    document_repository.add(document)

    # update the package content
    chosenPackage["jsonContent"]["content"].append(
        {"_id": blueprintId, "name": blueprintName, "type": "system/SIMOS/Blueprint"}
    )

    # update the package in the storage
    document_repository = get_data_source(chosenPackage["dataSourceId"])
    document: DTO = DTO(uid=chosenPackage["packageId"], data=chosenPackage["jsonContent"])
    document_repository.update(document)

    # update createdPackages and createdBlueprints in context
    for i in range(len(createdPackages)):
        if createdPackages[i]["jsonContent"]["name"] == packageName:
            createdPackages[i] = chosenPackage
    context.createdPackages = createdPackages
    context.createdBlueprints = context.createdBlueprints + [
        blueprint
    ]  # using an array makes it possible to create several packages in a single scenario.


@given('"{blueprintName}" has an optional attribute "{attributeName}" of type "{attributeType}"')
def append_attribute_to_blueprint(context, blueprintName: str, attributeName: str, attributeType: str):

    # find the correct blueprint
    chosenBlueprint: Dict
    createdBlueprints: [Dict] = context.createdBlueprints
    for blueprint in createdBlueprints:
        if blueprint["jsonContent"]["name"] == blueprintName:
            chosenBlueprint = blueprint

    # add a new entry to the blueprints' attributes list
    chosenBlueprint["jsonContent"]["attributes"].append(
        {
            "attributeType": attributeType,
            "type": "system/SIMOS/BlueprintAttribute",
            "name": attributeName,
            "optional": "true",
        }
    )

    # update the blueprint in storage
    document: DTO = DTO(uid=chosenBlueprint["blueprintId"], data=chosenBlueprint["jsonContent"])
    document_repository = get_data_source(chosenBlueprint["dataSourceId"])
    document_repository.update(document)

    # update the createdBlueprints array in context
    for i in range(len(createdBlueprints)):
        if createdBlueprints[i]["jsonContent"]["name"] == blueprintName:
            createdBlueprints[i] = chosenBlueprint
    context.createdBlueprints = createdBlueprints


# todo: avoid duplicate code in the below function


@given(
    '"{blueprintName}" has an optional array attribute "{attributeName}" of type "{attributeType}" with dimensions "{dimensions}"'
)
def append_attribute_to_blueprint(
    context, blueprintName: str, attributeName: str, attributeType: str, dimensions: str
):
    # find the correct blueprint
    chosenBlueprint: Dict
    createdBlueprints: [Dict] = context.createdBlueprints
    for blueprint in createdBlueprints:
        if blueprint["jsonContent"]["name"] == blueprintName:
            chosenBlueprint = blueprint

    # add a new entry to the blueprints' attributes list
    chosenBlueprint["jsonContent"]["attributes"].append(
        {
            "attributeType": attributeType,
            "type": "system/SIMOS/BlueprintAttribute",
            "name": attributeName,
            "optional": "true",
            "dimensions": dimensions,
        }
    )

    # update the blueprint in storage
    document: DTO = DTO(uid=chosenBlueprint["blueprintId"], data=chosenBlueprint["jsonContent"])
    document_repository = get_data_source(chosenBlueprint["dataSourceId"])
    document_repository.update(document)

    # update the createdBlueprints array in context
    for i in range(len(createdBlueprints)):
        if createdBlueprints[i]["jsonContent"]["name"] == blueprintName:
            createdBlueprints[i] = chosenBlueprint
    context.createdBlueprints = createdBlueprints
