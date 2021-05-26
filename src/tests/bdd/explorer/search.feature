Feature: Explorer - Search entity

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      | name       |
      | entities   |
      | blueprints |

    Given there are repositories in the data sources
      | data-source    | host | port  | username | password | tls   | name      | database | collection | type     | dataTypes |
      | entities       | db   | 27017 | maf      | maf      | false | repo1     | local    | entities   | mongo-db | default   |
      | blueprints     | db   | 27017 | maf      | maf      | false | blob-repo | local    | blueprints | mongo-db | default   |

    Given there exist document with id "1" in data source "blueprints"
    """
    {
        "name": "root_package",
        "description": "",
        "type": "system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
                "_id": "2",
                "name": "ValuesBlueprint",
                "type": "system/SIMOS/Blueprint"
            }
        ]
    }
    """
    Given there exist document with id "2" in data source "blueprints"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "ValuesBlueprint",
      "description": "This describes a blueprint that has a few different primitive attributes",
      "attributes": [
        {
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "name",
          "attributeType": "string",
          "optional": false
        },
        {
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "description",
          "attributeType": "string",
          "optional": false
        },
        {
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "type",
          "attributeType": "string",
          "default": "blueprints/root_package/ValuesBlueprint",
          "optional": false
        },
        {
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "a_number",
          "attributeType": "number",
          "default": "120",
          "optional": false
        },
        {
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "an_integer",
          "attributeType": "integer",
          "optional": false
        },
        {
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "a_string",
          "attributeType": "string",
          "optional": false
        }
      ]
    }
    """
    Given there exist document with id "1" in data source "entities"
    """
    {
      "name": "primitive_1",
      "description": "",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": 120.0,
      "an_integer": 5,
      "a_string": "abc"
    }
    """

    Given there exist document with id "2" in data source "entities"
    """
    {
      "name": "primitive_2",
      "description": "",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": 150.1,
      "an_integer": 10,
      "a_string": "def"
    }
    """

  Scenario: Search with primitive filter, all hit
    Given i access the resource url "/api/v1/search/entities"
    When i make a "POST" request
    """
    {
      "name": "PrImiT",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": ">100",
      "an_integer": "<11"
    }
    """
    Then the response status should be "OK"
    And the response should equal
    """
    {
      "primitive_2": {
        "_id": "2",
        "name": "primitive_2",
        "description": "",
        "type": "blueprints/root_package/ValuesBlueprint",
        "a_number": 150.1,
        "an_integer": 10,
        "a_string": "def"
      },
      "primitive_1": {
        "_id": "1",
        "name": "primitive_1",
        "description": "",
        "type": "blueprints/root_package/ValuesBlueprint",
        "a_number": 120.0,
        "an_integer": 5,
        "a_string": "abc"
      }
    }
    """
  Scenario: Search with primitive filter, 1 hit
    Given i access the resource url "/api/v1/search/entities"
    When i make a "POST" request
    """
    {
      "name": "PrImiT",
      "type": "blueprints/root_package/ValuesBlueprint",
      "a_number": ">121",
      "an_integer": ">5",
      "a_string": "de"
    }
    """
    Then the response status should be "OK"
    And the response should equal
    """
    {
      "primitive_2": {
        "_id": "2",
        "name": "primitive_2",
        "description": "",
        "type": "blueprints/root_package/ValuesBlueprint",
        "a_number": 150.1,
        "an_integer": 10,
        "a_string": "def"
      }
    }
    """
