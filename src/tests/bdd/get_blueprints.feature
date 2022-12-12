Feature: Get a blueprint

  Background: The core package is uploaded to the system
    Given the system data source and SIMOS core package are available
    Given the DMSS-lookup has been created


  Scenario: Get an extended simple blueprint
    Given I access the resource url "/api/v1/blueprint/dmss://system/SIMOS/Entity?context=DMSS"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
    "blueprint": {
      "name": "Entity",
      "description": "Blueprint for a DMT reference",
      "type": "dmss://system/SIMOS/Blueprint",
      "extends": ["dmss://system/SIMOS/DefaultUiRecipes", "dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "name": "name",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "description": "",
          "label": "Name",
          "default": "",
          "dimensions": "",
          "optional": false,
          "contained": true,
          "enumType": ""
        }, {
          "name": "type",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "description": "",
          "label": "Type",
          "default": "",
          "dimensions": "",
          "optional": false,
          "contained": true,
          "enumType": ""
        }, {
          "name": "description",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "description": "",
          "label": "Description",
          "default": "",
          "dimensions": "",
          "optional": true,
          "contained": true,
          "enumType": ""
        }
      ],
      "storageRecipes": [
        {
          "name": "Default",
          "storageAffinity": "default",
          "attributes": []
        }
      ],
      "uiRecipes": [
        {
          "name": "Yaml",
          "plugin": "yaml-view"
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

