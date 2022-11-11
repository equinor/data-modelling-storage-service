Feature: Get a blueprint

  Background: The core package is uploaded to the system
    Given the system data source and SIMOS core package are available

  Scenario: Get an extended simple blueprint
    Given I access the resource url "/api/v1/blueprint/sys://system/SIMOS/Entity"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "Entity",
      "description": "Blueprint for a DMT reference",
      "type": "sys://system/SIMOS/Blueprint",
      "extends": ["sys://system/SIMOS/DefaultUiRecipes", "sys://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "name": "name",
          "attributeType": "string",
          "type": "sys://system/SIMOS/BlueprintAttribute",
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
          "type": "sys://system/SIMOS/BlueprintAttribute",
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
          "type": "sys://system/SIMOS/BlueprintAttribute",
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
    }
    """

