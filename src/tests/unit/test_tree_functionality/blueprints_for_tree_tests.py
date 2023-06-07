from domain_classes.blueprint import Blueprint

all_contained_cases_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint1",
    "description": "First blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "description"},
        {"attributeType": "basic_blueprint", "type": "system/SIMOS/BlueprintAttribute", "name": "nested"},
        {"attributeType": "basic_blueprint", "type": "system/SIMOS/BlueprintAttribute", "name": "reference"},
        {
            "attributeType": "basic_blueprint",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "references",
            "dimensions": "*",
        },
    ],
}

basic_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint2",
    "description": "Second blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "description",
            "optional": True,
        },
        {"attributeType": "blueprint_3", "type": "system/SIMOS/BlueprintAttribute", "name": "nested"},
    ],
}

blueprint_3 = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint3",
    "description": "Second blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "description",
            "optional": True,
        },
        # This have to be optional, or else we will have an infinite loop caused by recursion
        {
            "attributeType": "basic_blueprint",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "reference",
            "optional": True,
            "contained": False,
        },
    ],
}

blueprint_4 = {
    "type": "system/SIMOS/Blueprint",
    "name": "Blueprint4",
    "description": "Second blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "name"},
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "description",
            "optional": True,
        },
        {
            "attributeType": "blueprint_4",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "a_list",
            "dimensions": "*",
        },
    ],
}

recursive_blueprint = {
    "type": "system/SIMOS/Blueprint",
    "name": "recursive",
    "description": "Second blueprint",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {"attributeType": "recursive_blueprint", "type": "system/SIMOS/BlueprintAttribute", "name": "im_me!"},
    ],
}

form_blueprint = {
    "name": "FormBlueprint",
    "type": "system/SIMOS/Blueprint",
    "attributes": [
        {"attributeType": "string", "type": "system/SIMOS/BlueprintAttribute", "name": "type"},
        {
            "name": "aNestedObject",
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "./NestedField",
            "label": "A nested object",
        },
        {
            "name": "aOptionalNestedObject",
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "./NestedField",
            "label": "A optional nested object",
            "optional": True,
        },
        {
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "inputEntity",
            "description": "Generic input entity",
            "attributeType": "object",
            "contained": False,
        },
    ],
}

signal_container_blueprint = {
    "name": "SignalContainer",
    "type": "system/SIMOS/Blueprint",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {"name": "cases", "attributeType": "Case", "dimensions": "*", "type": "CORE:BlueprintAttribute"},
    ],
}

case_blueprint = {
    "name": "Case",
    "type": "system/SIMOS/Blueprint",
    "extends": ["system/SIMOS/NamedEntity"],
    "attributes": [
        {"name": "signal", "attributeType": "Signal", "type": "CORE:BlueprintAttribute"},
    ],
}


signal_blueprint = {
    "name": "Signal",
    "type": "system/SIMOS/Blueprint",
    "attributes": [
        {"name": "values", "attributeType": "number", "dimensions": "*", "type": "CORE:BlueprintAttribute"},
    ],
}


def get_blueprint(type: str):
    if type == "all_contained_cases_blueprint":
        return Blueprint(all_contained_cases_blueprint)
    if type == "basic_blueprint":
        return Blueprint(basic_blueprint)
    if type == "blueprint_3":
        return Blueprint(blueprint_3)
    if type == "blueprint_4":
        return Blueprint(blueprint_4)
    if type == "recursive_blueprint":
        return Blueprint(recursive_blueprint)
    if type == "FormBlueprint":
        return Blueprint(form_blueprint)
    if type == "SignalContainer":
        return Blueprint(signal_container_blueprint)
    if type == "Case":
        return Blueprint(case_blueprint)
    if type == "Signal":
        return Blueprint(signal_blueprint)
    return None
