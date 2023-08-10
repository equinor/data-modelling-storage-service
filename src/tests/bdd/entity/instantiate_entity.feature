Feature: Instantiate entity

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      | name             |
      | data-source-name |
    Given there are repositories in the data sources
      | data-source       | host | port  | username | password | tls   | name     | database  | collection | type     | dataTypes |
      | data-source-name  | db   | 27017 | maf      | maf      | false | repo1    |  bdd-test | entities   | mongo-db | default   |

    Given there exist document with id "1" in data source "data-source-name"
    """
    {
      "name": "root_package",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "isRoot": true,
      "content": [
        {
          "address": "$2",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "storage"
        },
        {
          "address": "$3",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "storage"
        }
      ]
    }
    """


    Given there exist document with id "2" in data source "data-source-name"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "Employee",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "name": "isManager",
          "attributeType": "boolean",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        },
        {
          "name": "colleagues",
          "attributeType": "dmss://data-source-name/root_package/Employee",
          "optional": true,
          "dimensions": "*",
          "contained": false,
          "default": [],
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        },
        {
          "name": "salary",
          "attributeType": "integer",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true
        },
        {
          "name": "managers",
          "attributeType": "dmss://data-source-name/root_package/Employee",
          "optional": false,
          "dimensions": "*",
          "contained": false,
          "default": [
            {
              "address": "$5",
              "type": "dmss://system/SIMOS/Reference",
              "referenceType": "link"
            }
          ]
        },
        {
          "name": "bestFriendAtWork",
          "attributeType": "dmss://data-source-name/root_package/Employee",
          "optional": true,
          "contained": false,
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "default": {
            "type": "dmss://data-source-name/root_package/Employee",
            "name": "Kari",
            "isManager": false
          }
        }
      ]
    }
    """
    Given there exist document with id "3" in data source "data-source-name"
    """
    {
      "type": "dmss://data-source-name/root_package/Employee",
      "name": "BigBossMan",
      "isManager": true,
      "managers": []
    }
    """

  Scenario: instantiate entity
    Given i access the resource url "/api/entity"
    When i make a "POST" request
    """
    {
      "type": "dmss://data-source-name/root_package/Employee"
    }
    """
    Then the response status should be "OK"
    And the response should be
    """
    {
      "type": "dmss://data-source-name/root_package/Employee",
      "isManager": false,
      "name": "",
      "managers": [
        {
          "address": "$5",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
      ]
    }
    """