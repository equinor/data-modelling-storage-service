Feature: Validate Default Entity

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      | name             |
      | data-source-name |
    Given there are repositories in the data sources
      | data-source       | host | port  | username | password | tls   | name     | database  | collection | type     | dataTypes |
      | data-source-name  | db   | 27017 | maf      | maf      | false | repo1    |  bdd-test | entities   | mongo-db | default   |

    Given there exist document with id "root_package" in data source "data-source-name"
    """
    {
      "name": "root_package",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "isRoot": true,
      "content": [
        {
          "address": "$NorwegianBlueprint",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "storage"
        },
        {
          "address": "$PersonBlueprint",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "storage"
        },
        {
          "address": "$ChildBlueprint",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "storage"
        },
        {
          "address": "$AnimalBlueprint",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "storage"
        },
        {
          "address": "$SomeBlueprint",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "storage"
        }
      ]
    }
    """
    Given there exist document with id "NorwegianBlueprint" in data source "data-source-name"
    """
    {
      "name": "NorwegianBlueprint",
      "type": "dmss://system/SIMOS/Blueprint",
      "extends": ["dmss://data-source-name/root_package/PersonBlueprint"],
      "attributes": [
        {
          "name": "ski",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "string",
          "optional": false
        }
      ]
    }
    """

    Given there exist document with id "PersonBlueprint" in data source "data-source-name"
    """
    {
      "name": "PersonBlueprint",
      "type": "dmss://system/SIMOS/Blueprint",
      "attributes": [
        {
          "name": "type",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "string",
          "optional": false
        },
        {
          "name": "name",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "string",
          "label": "Name",
          "optional": false
        },
        {
          "name": "phoneNumber",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "integer",
          "label": "Phone number",
          "optional": true,
          "default": 123445566778
        },
        {
          "name": "nationality",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "string",
          "label": "Nationality",
          "optional": false,
          "default": "Norwegian"
        },
        {
          "name": "prime_minister",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://data-source-name/root_package/PersonBlueprint",
          "label": "Prime Minister",
          "optional": true,
          "default": {
            "type": "dmss://data-source-name/root_package/NorwegianBlueprint",
            "name": "Jonas",
            "nationality": "Norwegian",
            "ski": "Fisher"
          }
        },
        {
          "name": "address",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "number",
          "optional": true,
          "dimensions": "*",
          "contained": true,
          "default": [
            63.43, 10.39
          ]
        },
        {
          "name": "parents",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://data-source-name/root_package/PersonBlueprint",
          "optional": true,
          "dimensions": "*",
          "contained": true,
          "default": [
            {
              "type": "dmss://data-source-name/root_package/NorwegianBlueprint",
              "name": "Jonas",
              "nationality": "Norwegian",
              "ski": "Fisher"
            },
            {
              "type": "dmss://data-source-name/root_package/NorwegianBlueprint",
              "name": "Erna",
              "nationality": "Norwegian",
              "ski": "Madshus"
            }
          ]
        }
      ]
    }
    """

    Given there exist document with id "AnimalBlueprint" in data source "data-source-name"
    """
    {
      "name": "AnimalBlueprint",
      "type": "dmss://system/SIMOS/Blueprint",
      "extends": [
        "dmss://system/SIMOS/NamedEntity"
      ],
      "attributes": [
        {
          "name": "color",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "string",
          "label": "Color",
          "optional": false
        }
      ]
    }
    """

    Given there exist document with id "ChildBlueprint" in data source "data-source-name"
    """
    {
      "name": "ChildBlueprint",
      "type": "dmss://system/SIMOS/Blueprint",
      "extends": [
        "dmss://system/SIMOS/NamedEntity",
        "dmss://data-source-name/root_package/PersonBlueprint"
      ],
      "attributes": [
        {
          "name": "pet",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://data-source-name/root_package/AnimalBlueprint",
          "label": "Pet",
          "optional": false,
          "default": {
            "type": "dmss://data-source-name/root_package/NorwegianBlueprint",
            "name": "Jonas",
            "nationality": "Norwegian",
            "ski": "Fisher"
          }
        }
      ]
    }
    """

    Given there exist document with id "SomeBlueprint" in data source "data-source-name"
    """
    {
      "name": "SomeBlueprint",
      "type": "dmss://system/SIMOS/Blueprint",
      "attributes": [
        {
          "name": "pets",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "number",
          "label": "Number of pets",
          "optional": false,
          "default": "five"
        }
      ]
    }
    """

  Scenario: Validate existing simple example

    Given i access the resource url "/api/entity/validate-existing-entity/data-source-name/root_package/PersonBlueprint"
    When i make a "POST" request
    Then the response status should be "OK"

    Given i access the resource url "/api/entity/validate-existing-entity/data-source-name/root_package/ChildBlueprint"
    When i make a "POST" request
    Then the response status should be "Bad Request"
    And the response should contain
    """
    {
      "status": 400,
      "type": "ValidationException",
      "message": "Entity should be of type 'dmss://data-source-name/root_package/AnimalBlueprint' (or extending from it). Got 'dmss://data-source-name/root_package/NorwegianBlueprint'",
      "debug": "Location: Entity in key '^.attributes.0.default'",
      "data": {
        "name": "Jonas",
        "nationality": "Norwegian",
        "ski": "Fisher",
        "type": "dmss://data-source-name/root_package/NorwegianBlueprint"
        }
    }
    """

    Given i access the resource url "/api/entity/validate-existing-entity/data-source-name/root_package/SomeBlueprint"
    When i make a "POST" request
    Then the response status should be "Bad Request"
    And the response should contain
    """
    {
      "status": 400,
      "type": "ValidationException",
      "message": "Attribute 'default' should be type 'float'. Got 'str'. Value: five",
      "debug": "Location: Entity in key '^.attributes.0.default'",
      "data": null
    }
    """