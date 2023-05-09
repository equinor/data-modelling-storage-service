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

    Given there exist document with id "dmss://blueprints/$0f390843-3282-49fd-82fe-86ac668f241c"
    """
    {
        "name": "root_package",
        "description": "",
        "type": "dmss://system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
                "address": "dmss://blueprints/$0f390843-3282-49fd-82fe-86ac668f241d",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            }                                           
        ]
    }
    """
    Given there exist document with id "dmss://blueprints/$0f390843-3282-49fd-82fe-86ac668f241d"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "RecursiveBlueprint",
      "description": "This describes a blueprint that has a list of itself",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "name": "meAgain",
          "attributeType": "dmss://blueprints/root_package/RecursiveBlueprint",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "default": "[]",
          "dimensions": "*"
        }
      ]
    }
    """
    Given there exist document with id "dmss://entities/$0f390843-3282-49fd-82fe-86ac668f241a"
    """
    {
      "name": "recursiveTest",
      "description": "",
      "type": "dmss://blueprints/root_package/RecursiveBlueprint",
      "meAgain": [
        {
            "name": "level1-index0",
            "description": "",
            "type": "dmss://blueprints/root_package/RecursiveBlueprint",
            "diameter": 120,
            "pressure": 0,
            "meAgain": []
        },
        {
            "name": "level1-index1",
            "description": "",
            "type": "dmss://blueprints/root_package/RecursiveBlueprint",
            "diameter": 120,
            "pressure": 0,
            "meAgain": []
        }
      ]
    }
    """

  Scenario: Add nested contained node
    Given i access the resource url "/api/documents/entities/$0f390843-3282-49fd-82fe-86ac668f241a.meAgain.1.meAgain"
    When i make a "POST" request
    """
    {
      "name": "level2",
      "type": "dmss://blueprints/root_package/RecursiveBlueprint",
      "meAgain": []
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {"uid": "0f390843-3282-49fd-82fe-86ac668f241a.meAgain.1.meAgain.0"}
    """
