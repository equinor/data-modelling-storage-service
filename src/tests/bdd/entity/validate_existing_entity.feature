Feature: Validate entities in database

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
        },
        {
          "address": "$4",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "storage"
        },
        {
          "address": "$5",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "storage"
        },
        {
           "address": "$6",
           "type": "dmss://system/SIMOS/Reference",
           "referenceType": "storage"
        },
        {
          "address": "$7",
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
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """
    Given there exist document with id "3" in data source "data-source-name"
    """
    {
      "type": "dmss://data-source-name/root_package/Employee",
      "name": "Frodo",
      "isManager": false
    }
    """
    Given there exist document with id "4" in data source "data-source-name"
    """
    {
      "type": "dmss://data-source-name/root_package/Employee",
      "name": "John-Error",
      "age": 123
    }
    """
    Given there exist document with id "5" in data source "data-source-name"
    """
    {
      "type": "dmss://data-source-name/root_package/Employee",
      "name": "Sam",
      "isManager": true
    }
    """
    Given there exist document with id "6" in data source "data-source-name"
    """
    {
      "type": "dmss://data-source-name/root_package/Employee",
      "name": "Gandalf",
      "isManager": false,
      "colleagues": [
        {
          "address": "$3",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "storage"
        },
        {
          "address": "$5",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "storage"
        }
      ]
    }
    """
    Given there exist document with id "7" in data source "data-source-name"
    """
    {
      "type": "dmss://data-source-name/root_package/Employee",
      "name": "Saruman",
      "isManager": false,
      "colleagues": [
        {
          "address": "$4",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "storage"
        }
      ]
    }
    """



  Scenario: Validate existing correct entity
    Given i access the resource url "/api/entity/validate-existing-entity/data-source-name/root_package/Frodo"
    When i make a "POST" request
    Then the response status should be "OK"
    And the response should contain
    """
    "OK"
    """

  Scenario: Validate existing correct, complex entity
    Given i access the resource url "/api/entity/validate-existing-entity/data-source-name/root_package/Gandalf"
    When i make a "POST" request
    Then the response status should be "OK"
    And the response should contain
    """
    "OK"
    """

  Scenario: Validate existing entity with errors
    Given i access the resource url "/api/entity/validate-existing-entity/data-source-name/root_package/John-Error"
    When i make a "POST" request
    Then the response status should be "Bad Request"


  Scenario: Validate existing, complex entity with errors
    Given i access the resource url "/api/entity/validate-existing-entity/data-source-name/root_package/Saruman"
    When i make a "POST" request
    Then the response status should be "Bad Request"


  Scenario: Validate existing Package entity with errors
    Given i access the resource url "/api/entity/validate-existing-entity/data-source-name/root_package"
    When i make a "POST" request
    Then the response status should be "Bad Request"


