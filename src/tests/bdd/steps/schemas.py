import json
from typing import Dict

from behave import given


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



@given('there exists a package "{packageName}" with id "{uid}" in data source "{dataSourceId}"')
def create_package(context, packageName: str, dataSourceId: str, uid: str):
    package: Dict[Dict, str, str] = {
        'jsonContent': {
            'name': packageName,
            'description': 'Example package description',
            'type': 'system/SIMOS/Package',
            'content': [],
            'isRoot': 'true',
            'storageRecipes':[],
            'uiRecipes':[]
        }, 
        'dataSourceId': dataSourceId, 
        'packageId': uid
        }
    

    context.createdPackages = context.createdPackages + [package] # using an array makes it possible to create several packages in a single scenario.
    document: DTO = DTO(uid=package['packageId'], data=package['jsonContent'])
    document_repository = get_data_source(package['dataSourceId'])
    document_repository.add(document)


# a "bare minimum blueprint" = a blueprint with only required attributes (name and type)
@given('the package "{packageName}" contains a bare minimum blueprint "{blueprintName}" with id "{blueprintId}"')
def append_blueprint_to_package(context, packageName: str, blueprintName: str, blueprintId: str):

    #find the package to add the blueprint to
    chosenPackage: Dict
    createdPackages: [Dict] = context.createdPackages
    for package in createdPackages:
        if package['jsonContent']['name'] == packageName:
            chosenPackage = package

    blueprint: Dict =  {
        'jsonContent': {
            'type': 'system/SIMOS/Blueprint',
            'name': blueprintName,
            'description': '',
            'attributes': [
                {
                'attributeType': 'string', 
                'type': 'system/SIMOS/BlueprintAttribute',
                'name': 'name'
                },
                {
                'attributeType': 'string',
                'type': 'system/SIMOS/BlueprintAttribute',
                'name': 'type'
                },
            ],
            'storageRecipes':[],
            'uiRecipes':[]
        },
        'blueprintId': blueprintId,
        'dataSourceId': chosenPackage['dataSourceId']
    }

    #add blueprint to storage
    document: DTO = DTO(uid=blueprint['blueprintId'], data=blueprint['jsonContent'])
    document_repository = get_data_source(blueprint['dataSourceId']) #question: can package and blueprint have different data sources???
    document_repository.add(document)

    # update the package content
    chosenPackage['jsonContent']['content'].append({'_id': blueprintId, 'name': blueprintName, 'type': 'system/SIMOS/Blueprint'})
    
    # update the package in the storage
    document_repository = get_data_source(chosenPackage['dataSourceId'])
    document: DTO = DTO(uid=chosenPackage['packageId'], data=chosenPackage['jsonContent'])
    document_repository.update(document)

    #update createdPackages and createdBlueprints in context
    for i in range(len(createdPackages)):
        if createdPackages[i]['jsonContent']['name'] == packageName:
            createdPackages[i] = chosenPackage
    context.createdPackages = createdPackages
    context.createdBlueprints = context.createdBlueprints + [blueprint] # using an array makes it possible to create several packages in a single scenario.



@given('"{blueprintName}" has an optional attribute "{attributeName}" of type "{attributeType}"')
def append_attribute_to_blueprint(context, blueprintName: str, attributeName: str, attributeType: str):
    
    #find the correct blueprint
    chosenBlueprint: Dict
    createdBlueprints: [Dict] = context.createdBlueprints
    for blueprint in createdBlueprints:
        if blueprint['jsonContent']['name'] == blueprintName:
            chosenBlueprint = blueprint


    # add a new entry to the blueprints' attributes list
    chosenBlueprint['jsonContent']['attributes'].append({'attributeType': attributeType, 'type': 'system/SIMOS/BlueprintAttribute', 'name': attributeName, 'optional': 'true'})

    # update the blueprint in storage
    document: DTO = DTO(uid=chosenBlueprint['blueprintId'], data=chosenBlueprint['jsonContent'])
    document_repository = get_data_source(chosenBlueprint['dataSourceId']) 
    document_repository.update(document)


    #update the createdBlueprints array in context
    for i in range(len(createdBlueprints)):
        if createdBlueprints[i]['jsonContent']['name'] == blueprintName:
            createdBlueprints[i] = chosenBlueprint
    context.createdBlueprints = createdBlueprints
    
#todo: avoid duplicate code in the below function

@given('"{blueprintName}" has an optional array attribute "{attributeName}" of type "{attributeType}" with dimensions "{dimensions}"')
def append_attribute_to_blueprint(context, blueprintName: str, attributeName: str, attributeType: str, dimensions: str):
    #find the correct blueprint
    chosenBlueprint: Dict
    createdBlueprints: [Dict] = context.createdBlueprints
    for blueprint in createdBlueprints:
        if blueprint['jsonContent']['name'] == blueprintName:
            chosenBlueprint = blueprint


    # add a new entry to the blueprints' attributes list
    chosenBlueprint['jsonContent']['attributes'].append({'attributeType': attributeType, 'type': 'system/SIMOS/BlueprintAttribute', 'name': attributeName, 'optional': 'true', 'dimensions': dimensions})

    # update the blueprint in storage
    document: DTO = DTO(uid=chosenBlueprint['blueprintId'], data=chosenBlueprint['jsonContent'])
    document_repository = get_data_source(chosenBlueprint['dataSourceId']) 
    document_repository.update(document)


    #update the createdBlueprints array in context
    for i in range(len(createdBlueprints)):
        if createdBlueprints[i]['jsonContent']['name'] == blueprintName:
            createdBlueprints[i] = chosenBlueprint
    context.createdBlueprints = createdBlueprints
    