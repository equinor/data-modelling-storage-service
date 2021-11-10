Feature: Explorer - Add contained node

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available

    Given there are data sources
      | name       |
      | entities   |
      | blueprints |

    Given there are repositories in the data sources
      | data-source    | host | port  | username | password | tls   | name      | database | collection | type     | dataTypes |
      | entities       | db   | 27017 | maf      | maf      | false | repo1     |  bdd-test    | entities   | mongo-db | default   |
      | blueprints     | db   | 27017 | maf      | maf      | false | blob-repo |  bdd-test    | blueprints | mongo-db | default   |

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
                "name": "RecursiveBlueprint",
                "type": "system/SIMOS/Blueprint"
            }
        ]
    }
    """
    Given there exist document with id "2" in data source "blueprints"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "RecursiveBlueprint",
      "description": "This describes a blueprint that has a list of itself",
      "attributes": [
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "name",
          "optional": false
        },
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "description",
          "optional": false
        },
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "type",
          "optional": false,
          "default": "blueprints/root_package/RecursiveBlueprint"
        },
        {
          "name": "meAgain",
          "attributeType": "blueprints/root_package/RecursiveBlueprint",
          "type": "system/SIMOS/BlueprintAttribute",
          "default": "[]",
          "dimensions": "*",
          "optional": true
        }
      ]
    }
    """
    Given there exist document with id "1" in data source "entities"
    """
    {
      "name": "recursiveTest",
      "description": "",
      "type": "blueprints/root_package/RecursiveBlueprint",
      "meAgain": [
        {
            "name": "level1-index0",
            "description": "",
            "type": "blueprints/root_package/RecursiveBlueprint",
            "diameter": 120,
            "pressure": 0,
            "meAgain": []
        },
        {
            "name": "level1-index1",
            "description": "",
            "type": "blueprints/root_package/RecursiveBlueprint",
            "diameter": 120,
            "pressure": 0,
            "meAgain": []
        }
      ]
    }
    """

  Scenario: Add nested contained node
    Given i access the resource url "/api/v1/explorer/entities/1.meAgain.1.meAgain"
    When i make a "POST" request
    """
    {
      "name": "level2",
      "type": "blueprints/root_package/RecursiveBlueprint",
      "description": ""
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {"uid": "1.meAgain.1.meAgain.0"}
    """
