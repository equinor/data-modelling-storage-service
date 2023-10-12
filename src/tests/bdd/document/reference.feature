Feature: Add and remove references

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |

  Scenario: Insert and remove reference (in list)
    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "name": "TestData",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "content": [],
      "isRoot": true
    }
    """

    Given there exist document with id "5" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "some-blueprint",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "description": "just some blueprint",
      "attributes": []
    }
    """

    Given i access the resource url "/api/documents/test-DS/$1.content"
    When i make a form-data "POST" request
    """
    {
      "document":
        {
          "address": "$5",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
    }
    """
    Then the response status should be "OK"

    Given i access the resource url "/api/documents/test-DS/$1"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "TestData",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "content": [
        {
          "address": "$5",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
      ],
      "isRoot": true
    }
    """

    Given i access the resource url "/api/documents/test-DS/$1.content[0]"
    When i make a "DELETE" request
    Then the response status should be "OK"

    Given i access the resource url "/api/documents/test-DS/$1"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "TestData",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "content": [],
      "isRoot": true
    }
    """

  Scenario: Insert and remove reference (simple)
    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "name": "TestData",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "content": [
        {
          "address": "$turbineBlueprint",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        },
        {
          "address": "$mooringBlueprint",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        },
        {
          "address": "$turbineEntity",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        },
        {
          "address": "$mooringEntity1",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        },
        {
          "address": "$mooringEntity2",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
      ],
      "isRoot": true
    }
    """

    Given there exist document with id "turbineBlueprint" in data source "test-DS"
    """
    {
      "name": "Turbine",
      "type": "dmss://system/SIMOS/Blueprint",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "description": "",
      "attributes": [
        {
          "name": "Mooring",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://test-DS/TestData/Mooring",
          "optional": true,
          "contained": false
        }
      ]
    }
    """

    Given there exist document with id "mooringBlueprint" in data source "test-DS"
    """
    {
      "name": "Mooring",
      "type": "dmss://system/SIMOS/Blueprint",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "description": "",
      "attributes": [
        {
          "name": "Bigness",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "description": "How big? Very",
          "attributeType": "integer",
          "contained": true
        }
      ]
    }
    """

    Given there exist document with id "turbineEntity" in data source "test-DS"
    """
    {
      "name": "myTurbine",
      "type": "dmss://test-DS/TestData/Turbine",
      "description": "This is a wind turbine demoing uncontained relationships"
    }
    """

    Given there exist document with id "mooringEntity1" in data source "test-DS"
    """
    {
    "name": "mooring1",
    "type": "dmss://test-DS/TestData/Mooring",
    "description": "",
    "Bigness": 10
    }
    """

    Given there exist document with id "mooringEntity2" in data source "test-DS"
    """
    {
    "name": "mooring2",
    "type": "dmss://test-DS/TestData/Mooring",
    "description": "",
    "Bigness": 100
    }
    """

    Given i access the resource url "/api/documents/test-DS/$turbineEntity.Mooring"
    When i make a form-data "POST" request
    """
    {
      "document": {
        "address": "$mooringEntity1",
        "type": "dmss://system/SIMOS/Reference",
        "referenceType": "link"
      }
    }
    """
    Then the response status should be "OK"

    Given i access the resource url "/api/documents/test-DS/$turbineEntity"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "myTurbine",
      "type": "dmss://test-DS/TestData/Turbine",
      "description": "This is a wind turbine demoing uncontained relationships",
      "Mooring": {
        "address": "$mooringEntity1",
        "type": "dmss://system/SIMOS/Reference",
        "referenceType": "link"
      }
    }
    """

    Given i access the resource url "/api/documents/test-DS/$turbineEntity.Mooring"
    When i make a form-data "PUT" request
    """
    {
      "data": {
        "address": "$mooringEntity2",
        "type": "dmss://system/SIMOS/Reference",
        "referenceType": "link"
      }
    }
    """
    Then the response status should be "OK"

    Given i access the resource url "/api/documents/test-DS/$turbineEntity"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "myTurbine",
      "type": "dmss://test-DS/TestData/Turbine",
      "description": "This is a wind turbine demoing uncontained relationships",
      "Mooring": {
        "address": "$mooringEntity2",
        "type": "dmss://system/SIMOS/Reference",
        "referenceType": "link"
      }
    }
    """

    Given i access the resource url "/api/documents/test-DS/$turbineEntity.Mooring"
    When i make a "DELETE" request
    Then the response status should be "OK"

    Given i access the resource url "/api/documents/test-DS/$turbineEntity"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "myTurbine",
      "type": "dmss://test-DS/TestData/Turbine",
      "description": "This is a wind turbine demoing uncontained relationships"
    }
    """

    Scenario: Replace reference in entity
    Given there exist document with id "10" in data source "test-DS"
    """
    {
      "name": "TestReplace",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "content": [
        {
          "address": "$Company",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        },
        {
          "address": "$Person",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        },
        {
          "address": "$companyEntity",
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link"
        }
      ],
      "isRoot": true
    }
    """

    Given there exist document with id "Company" in data source "test-DS"
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
          "attributeType": "dmss://test-DS/TestReplace/Person",
          "dimensions": "*",
          "label": "Employees"
        },
        {
          "name": "ceo",
          "type": "CORE:BlueprintAttribute",
          "attributeType": "dmss://test-DS/TestReplace/Person",
          "label": "CEO",
          "contained": false,
          "optional": false
        },
        {
          "name": "accountant",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://test-DS/TestReplace/Person",
          "label": "Accountant",
          "contained": false,
          "optional": false
        }
      ]
    }
    """

    Given there exist document with id "Person" in data source "test-DS"
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

    Given there exist document with id "companyEntity" in data source "test-DS"
    """
    {
      "name": "myCompany",
      "type": "dmss://test-DS/TestReplace/Company",
      "employees": [
        {
          "name": "Miranda",
          "type": "dmss://test-DS/TestReplace/Person",
          "phoneNumber": 1337
        },
        {
          "name": "John",
          "type": "dmss://test-DS/TestReplace/Person",
          "phoneNumber": 1234
        }
      ],
      "ceo": {
        "type": "dmss://system/SIMOS/Reference",
        "address": "^.employees[0]",
        "referenceType": "link"
      },
      "accountant": {
        "type": "dmss://system/SIMOS/Reference",
        "address": "^.employees[0]",
        "referenceType": "link"
      }
    }
    """

    Given there exist document with id "personEntity1" in data source "test-DS"
    """
    {
      "name": "personEntity1",
      "type": "dmss://test-DS/TestReplace/Person",
      "phoneNumber": 1337
    }
    """

    Given i access the resource url "/api/documents/test-DS/$companyEntity"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "myCompany",
      "type": "dmss://test-DS/TestReplace/Company",
      "employees": [
        {
          "name": "Miranda",
          "type": "dmss://test-DS/TestReplace/Person",
          "phoneNumber": 1337
        },
        {
          "name": "John",
          "type": "dmss://test-DS/TestReplace/Person",
          "phoneNumber": 1234
        }
      ],
      "accountant": {
        "type": "dmss://system/SIMOS/Reference",
        "address": "^.employees[0]",
        "referenceType": "link"
      }
    }
    """

    Given i access the resource url "/api/documents/test-DS/$companyEntity.accountant"
    When i make a form-data "PUT" request
    """
    {
      "data": {
        "address": "$companyEntity.employees[1]",
        "type": "dmss://system/SIMOS/Reference",
        "referenceType": "link"
      }
    }
    """
    Then the response status should be "OK"

    Given i access the resource url "/api/documents/test-DS/$companyEntity"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "myCompany",
      "type": "dmss://test-DS/TestReplace/Company",
      "employees": [
        {
          "name": "Miranda",
          "type": "dmss://test-DS/TestReplace/Person",
          "phoneNumber": 1337
        },
        {
          "name": "John",
          "type": "dmss://test-DS/TestReplace/Person",
          "phoneNumber": 1234
        }
      ],
      "accountant": {
        "type": "dmss://system/SIMOS/Reference",
        "address": "$companyEntity.employees[1]",
        "referenceType": "link"
      }
    }
    """