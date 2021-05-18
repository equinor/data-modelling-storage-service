Feature: Explorer - Add contained node

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
      | system         | db   | 27017 | maf      | maf      | false | system    | local    | system     | mongo-db | default   |

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
          "dimensions": "*"
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
    Given i access the resource url "/api/v1/explorer/entities/add-to-parent"
    When i make a "POST" request
    """
    {
      "name": "level2",
      "parentId": "1",
      "type": "blueprints/root_package/RecursiveBlueprint",
      "attribute": "meAgain.1.meAgain"
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {"uid": "1.meAgain.1.meAgain.0"}
    """
    # Given I access the resource url "/api/v4/index/entities/1.meAgain.1/1.meAgain.1.meAgain"
    # When I make a "GET" request
    # Then the response status should be "OK"
    # And the response should contain
    # """
    # {
    #    "1.meAgain.1.meAgain": {
    #       "parentId": "1.meAgain.1",
    #       "title": "meAgain",
    #       "id": "1.meAgain.1.meAgain",
    #       "nodeType": "document-node",
    #       "children": [ ],
    #       "type": "blueprints/root_package/RecursiveBlueprint"
    #    }
    # }
    # """
