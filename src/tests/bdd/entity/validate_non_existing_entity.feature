Feature: Validate entities not in the database

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
      "name": "root_employee_package",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "isRoot": true,
      "content": [
        {
          "address": "$2",
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
          "attributeType": "dmss://data-source-name/root_employee_package/Employee",
          "optional": true,
          "dimensions": "*",
          "contained": false,
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """



  Scenario: Validate non-existing entity
    Given i access the resource url "/api/entity/validate"
    When i make a "POST" request
    """
    {
      "type": "dmss://data-source-name/root_employee_package/Employee",
      "name": "Ola",
      "isManager": false
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    "OK"
    """

  Scenario: Validate non-existing entity with error
    Given i access the resource url "/api/entity/validate"
    When i make a "POST" request
    """
    {
      "type": "dmss://data-source-name/root_employee_package/Employee",
      "name": "Kari",
      "age": 123
    }
    """
    Then the response status should be "Bad Request"

    Scenario: Validate another non-existing entity with error
    Given i access the resource url "/api/entity/validate"
    When i make a "POST" request
    """
    {
      "type": "dmss://data-source-name/root_employee_package/Employee",
      "name": "Nora",
      "salary": 123
    }
    """
    Then the response status should be "Bad Request"


    Scenario: Validate a complex non-existing entity
    Given i access the resource url "/api/entity/validate"
    When i make a "POST" request
    """
    {
      "type": "dmss://data-source-name/root_employee_package/Employee",
      "name": "Legolas",
      "isManager": false,
      "colleagues": [
        {
          "address": "$5",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
      ]
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    "OK"
    """
