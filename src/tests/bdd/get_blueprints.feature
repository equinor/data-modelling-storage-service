Feature: Get a blueprint

  Background: The core package is uploaded to the system
    Given the system data source and SIMOS core package are available
#    Given the DMSS-lookup has been created
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |

    Given there are repositories in the data sources
      | data-source | host | port  | username | password | tls   | name  | database  | collection | type     | dataTypes |
      |  test-DS    | db   | 27017 | maf      | maf      | false | blobs |  bdd-test | blobs      | mongo-db | blob      |



   Given there exist document with id "1" in data source "test-DS"
    """
    {
        "name": "root_package",
        "type": "dmss://system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
                "address": "$2",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$3",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            }
        ]
    }
    """
    Given there exist document with id "2" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "BlueprintWithManyDefaultValues",
      "attributes": [
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "name",
          "attributeType": "string",
          "default": "exampleName",
          "optional": false
        },
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "type",
          "attributeType": "string",
          "default": "blueprints/root_package/ValuesBlueprint",
          "optional": false
        },
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "a_number",
          "attributeType": "number",
          "default": 120.44,
          "optional": false
        },
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "an_integer",
          "attributeType": "integer",
          "default": 33,
          "optional": false
        },
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "a_bool",
          "attributeType": "boolean",
          "default": false,
          "optional": false
        },
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "a_list",
          "attributeType": "boolean",
          "dimensions": "*",
          "default": [false, true, false],
          "optional": false
        },
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "an_entity",
          "attributeType": "test-DS/root_package/ExampleBlueprint",
          "default": {
            "name": "foo",
            "type": "test-DS/root_package/ExampleBlueprint",
            "AValue": 123
          }
        }
      ]
    }
    """
    Given there exist document with id "3" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "ExampleBlueprint",
      "description": "",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
        "name": "AValue",
        "attributeType": "integer",
        "type": "dmss://system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """


  Scenario: Get a blueprint with many default values
    Given I access the resource url "/api/blueprint/dmss://test-DS/root_package/BlueprintWithManyDefaultValues"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
    "blueprint": {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "BlueprintWithManyDefaultValues",
      "attributes": [
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "name",
          "attributeType": "string",
          "default": "exampleName",
          "optional": false
        },
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "type",
          "attributeType": "string",
          "default": "blueprints/root_package/ValuesBlueprint",
          "optional": false
        },
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "a_number",
          "attributeType": "number",
          "default": 120.44,
          "optional": false
        },
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "an_integer",
          "attributeType": "integer",
          "default": 33,
          "optional": false
        },
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "a_bool",
          "attributeType": "boolean",
          "default": false,
          "optional": false
        },
        {
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "a_list",
          "attributeType": "boolean",
          "dimensions": "*",
          "default": [false, true, false],
          "optional": false
        }
      ]
    }
    }
    """


  Scenario: Get a simple blueprint with a ui recipe from a recipe context
    Given I access the resource url "/api/blueprint/dmss://system/SIMOS/Entity?context=DMSS"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
    "blueprint": {
      "name": "Entity",
      "description": "Blueprint for a DMT reference",
      "type": "dmss://system/SIMOS/Blueprint",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "name": "name",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        }, {
          "name": "type",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        }, {
          "name": "description",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    }
    """


  Scenario: Get a simple blueprint with a default ui recipe from a recipe context
    Given I access the resource url "/api/blueprint/dmss://system/SIMOS/Blob?context=DMSS"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "blueprint": {
        "name": "Blob",
        "type": "dmss://system/SIMOS/Blueprint",
        "extends": [
          "dmss://system/SIMOS/NamedEntity"
        ],
        "description": "Reference to a BLOB",
        "attributes": [
          {
            "name": "name",
            "optional": false,
            "attributeType": "string",
            "type": "dmss://system/SIMOS/BlueprintAttribute"
          },
          {
            "name": "type",
            "attributeType": "string",
            "type": "dmss://system/SIMOS/BlueprintAttribute"
          },
          {
            "name": "description",
            "attributeType": "string",
            "type": "dmss://system/SIMOS/BlueprintAttribute"
          },
          {
            "name": "_meta_",
            "attributeType": "dmss://system/SIMOS/Meta",
            "type": "dmss://system/SIMOS/BlueprintAttribute"
          },
          {
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "name": "_blob_id",
            "description": "id for the raw blob",
            "attributeType": "string",
            "contained": true
          },
          {
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "name": "size",
            "description": "Size of the blob in bytes",
            "attributeType": "integer",
            "default": 0,
            "optional": true,
            "contained": true
          }
        ]
      }
    }
    """

  Scenario: Get a simple blueprint with no specified recipe context given should give the default recipes
    Given I access the resource url "/api/blueprint/dmss://system/SIMOS/Entity"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
    "uiRecipes":[
    {
      "name": "Edit",
      "type": "dmss://system/SIMOS/UiRecipe",
      "plugin": "@development-framework/dm-core-plugins/form"
    },
    {
      "name": "Yaml",
      "type": "dmss://system/SIMOS/UiRecipe",
      "plugin": "@development-framework/dm-core-plugins/yaml"
    },
    {
      "name": "List",
      "type": "dmss://system/SIMOS/UiRecipe",
      "plugin": "@development-framework/dm-core-plugins/list",
      "dimensions": "*"
    }
    ],
    "blueprint": {
      "name": "Entity",
      "description": "Blueprint for a DMT reference",
      "type": "dmss://system/SIMOS/Blueprint",
      "extends": [ "dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "name": "name",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": false,
          "contained": true
        }, {
          "name": "type",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        }, {
          "name": "description",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        }, {
            "name": "_meta_",
            "attributeType": "dmss://system/SIMOS/Meta",
            "type": "dmss://system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    }
    """

