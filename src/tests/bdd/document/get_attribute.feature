# Created by CHCL at 09/01/2024
Feature: Get an attribute
  # Enter feature description here
  Background: The core package is uploaded to the system
    Given the system data source and SIMOS core package are available
#    Given the DMSS-lookup has been created
    Given there are basic data sources with repositories
      | name    |
      | test-DS |

    Given there are repositories in the data sources
      | data-source | host | port  | username | password | tls   | name  | database | collection | type     | dataTypes |
      | test-DS     | db   | 27017 | maf      | maf      | false | blobs | bdd-test | blobs      | mongo-db | blob      |



    Given there exist document with id "1" in data source "test-DS"
    """
    {
        "name": "root_package",
        "type": "dmss://system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
                "address": "$2",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$3",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$4",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$5",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            }
        ]
    }
    """
    Given there exist document with id "2" in data source "test-DS"
    """
    {
      "name": "Company",
      "type": "dmss://system/SIMOS/Blueprint",
      "attributes": [
        {
          "name": "type",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "string"
        },
        {
          "name": "name",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "string"
        },
        {
          "name": "employees",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://test-DS/root_package/Person",
          "dimensions": "*",
          "label": "Employees"
        },
        {
          "name": "ceo",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://test-DS/root_package/Person",
          "label": "CEO",
          "contained": false,
          "optional": false
        },
        {
          "name": "numberOfEmployees",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "number",
          "contained": true,
          "optional": true
        },
        {
          "name": "accountant",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://test-DS/root_package/Person",
          "label": "Accountant",
          "contained": false,
          "optional": false
        },
        {
          "name": "averageSalary",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "number",
          "contained": true,
          "optional": true
        },
        {
          "name": "assistant",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://test-DS/root_package/Person",
          "label": "Assistant",
          "contained": false,
          "optional": true
        },
        {
          "name": "trainee",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://test-DS/root_package/Person",
          "label": "Trainee",
          "contained": false,
          "optional": true
        },
        {
          "name": "description",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "string",
          "contained": true,
          "optional": true
        },
        {
          "name": "middleManager",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://test-DS/root_package/Manager",
          "contained": true,
          "optional": true
        }
      ]
    }
    """

    Given there exist document with id "3" in data source "test-DS"
    """
    {
      "type":"dmss://test-DS/root_package/Company",
      "_id":"UncontainedObject",
      "name":"UncontainedObject",
      "numberOfEmployees":10,
      "averageSalary":800000,
      "description":"It's a super nice place to work. The people are happy and they love to create great applications for use in the moorling line simulations.",
      "employees":[
        {
          "type":"dmss://test-DS/root_package/Person",
          "name":"Miranda",
          "phoneNumber":1337
        },
        {
          "type":"dmss://test-DS/root_package/Person",
          "name":"John","phoneNumber":1234
      }],
      "ceo":{
        "type":"dmss://system/SIMOS/Reference",
        "referenceType":"link",
        "address":"^.employees[0]"
      },
      "accountant":{
        "type":"dmss://system/SIMOS/Reference",
        "referenceType":"link",
        "address":"^.employees[0]"
      },
      "assistant":{
        "type":"dmss://system/SIMOS/Reference",
        "referenceType":"link",
        "address":"dmss://test-DS/$3.accountant"
      },
      "middleManager": {
        "type":"dmss://test-DS/root_package/Manager",
        "name":"Karen",
        "phoneNumber":1337,
        "worker": {
          "type":"dmss://system/SIMOS/Reference",
          "referenceType":"link",
          "address":"^.employees[1]"
        }
      }
    }
    """
    Given there exist document with id "4" in data source "test-DS"
    """
    {
      "name": "Person",
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
          "attributeType": "number",
          "label": "Phone Number",
          "optional": true
        }
      ]
    }
    """
  Given there exist document with id "5" in data source "test-DS"
    """
    {
      "name": "Manager",
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
          "attributeType": "number",
          "label": "Phone Number",
          "optional": true
        },
        {
          "name": "worker",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://test-DS/root_package/Person",
          "label": "Worker",
          "optional": true,
          "contained": false
        }
      ]
    }
    """
  Scenario: Get contained attribute with resolve
    Given I access the resource url "/api/attribute/test-DS/$3.employees?resolve=true"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
      {
        "attribute": {
          "name": "employees",
          "attributeType": "dmss://test-DS/root_package/Person",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "description": "",
          "label": "Employees",
          "default": null,
          "dimensions": "*",
          "optional": false,
          "contained": true,
          "enumType": ""
        },
        "address": "test-DS/$3.employees"
      }
    """
  Scenario: Get contained attribute without resolve
    Given I access the resource url "/api/attribute/test-DS/$3.employees?resolve=false"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
      {
        "attribute": {
          "name": "employees",
          "attributeType": "dmss://test-DS/root_package/Person",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "description": "",
          "label": "Employees",
          "default": null,
          "dimensions": "*",
          "optional": false,
          "contained": true,
          "enumType": ""
        },
        "address": "test-DS/$3.employees"
      }
    """
  Scenario: Get uncontained attribute with resolve
    Given I access the resource url "/api/attribute/test-DS/$3.ceo?resolve=true"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
      {
        "attribute":{
          "name": "employees",
          "attributeType": "dmss://test-DS/root_package/Person",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "description": "",
          "label": "Employees",
          "default": null,
          "dimensions": "",
          "optional": false,
          "contained": true,
          "enumType": ""
        },
        "address": "dmss://test-DS/$3.employees[0]"
      }
    """
  Scenario: Get uncontained attribute without resolve
    Given I access the resource url "/api/attribute/test-DS/$3.ceo?resolve=false"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
      {
        "attribute": {
          "name": "ceo",
          "attributeType": "dmss://system/SIMOS/Reference",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "description": "",
          "label": "CEO",
          "default": null,
          "dimensions": "",
          "optional": false,
          "contained": false,
          "enumType": ""
        },
        "address": "test-DS/$3.ceo"
      }
    """
  Scenario: Get nested uncontained attribute without resolve
    Given I access the resource url "/api/attribute/test-DS/$3.middleManager.worker?resolve=true"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
      {
        "attribute": {
          "name": "employees",
          "attributeType": "dmss://test-DS/root_package/Person",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "description": "",
          "label": "Employees",
          "default": null,
          "dimensions": "",
          "optional": false,
          "contained": true,
          "enumType": ""
        },
        "address": "dmss://test-DS/$3.employees[1]"
      }
    """