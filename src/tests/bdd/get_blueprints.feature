Feature: Get a blueprint

  Background: The core package is uploaded to the system
    Given the system data source and SIMOS core package are available
#    Given the DMSS-lookup has been created


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
    },
    "uiRecipes": [
      {
        "type": "dmss://system/SIMOS/UiRecipe",
        "name": "DEFAULT_CREATE",
        "description": "",
        "attributes": [
          {
            "name": "type",
            "attributeType": "string",
            "type": "dmss://system/SIMOS/UiAttribute",
            "field": "blueprint",
            "label": "Type"
          }
        ]
      }
    ],
     "storageRecipes": []
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
            "default": "0",
            "optional": true,
            "contained": true
          }
        ]
      },
      "uiRecipes": [
        {
          "name": "Yaml",
          "type": "dmss://system/SIMOS/UiRecipe",
          "plugin": "yaml",
          "roles": [
            "dmss-admin"
          ],
          "category": "view"
        },
        {
          "name": "Edit",
          "type": "dmss://system/SIMOS/UiRecipe",
          "plugin": "form",
          "category": "edit"
        }
      ],
      "storageRecipes": []
    }
    """

  Scenario: Get a simple blueprint with no specified recipe context given should give the default recipes
    Given I access the resource url "/api/blueprint/dmss://system/SIMOS/Entity"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
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
        }
      ]
    },
    "uiRecipes": [
      {
        "name": "Edit",
        "type": "dmss://system/SIMOS/UiRecipe",
        "plugin": "form",
        "category": "edit"
      },
      {
        "name": "Yaml",
        "type": "dmss://system/SIMOS/UiRecipe",
        "plugin": "yaml",
        "category": "view"
      }
    ],
    "storageRecipes": []
    }
    """

