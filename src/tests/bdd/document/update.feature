Feature: Document 2

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available

    Given there are data sources
      |       name         |
      | data-source-name   |
      | test-source-name   |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name       | database | collection | type     | dataTypes    |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1      |  bdd-test    | documents  | mongo-db | default      |
      | test-source-name | db   | 27017 | maf      | maf      | false | blob-repo  |  bdd-test    | blob-data  | mongo-db | default,blob |
      | data-source-name | db   | 27017 | maf      | maf      | false | doc-repo   |  bdd-test    | test       | mongo-db | default      |


    Given there exist document with id "2" in data source "test-source-name"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "ItemType",
      "description": "",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "extra"
        },
        {
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "list",
          "dimensions" : "*"
        },
        {
          "attributeType": "dmss://test-source-name/TestData/ItemTypeTwo",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "complexList",
          "dimensions" : "*"
        }
      ]
    }
    """

    Given there exist document with id "4" in data source "test-source-name"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "ItemTypeTwo",
      "description": "",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "extra"
        },
        {
          "attributeType": "object",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "complexAttribute"
        }
      ]
    }
    """

    Given there exist document with id "3" in data source "test-source-name"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "TestContainer",
      "description": "",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "attributeType": "dmss://test-source-name/TestData/ItemType",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "itemContained"
        },
        {
          "attributeType": "dmss://test-source-name/TestData/ItemType",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "dimensions": "*",
          "name": "itemsContained"
        },
        {
          "attributeType": "dmss://test-source-name/TestData/ItemType",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "itemNotContained"
        },
        {
          "attributeType": "dmss://test-source-name/TestData/ItemType",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "dimensions": "*",
          "name": "itemsNotContained"
        }
      ]
    }
    """

    Given there exist document with id "1" in data source "test-source-name"
    """
    {
        "name": "TestData",
        "description": "",
        "type": "dmss://system/SIMOS/Package",
        "content": [
            {
                "address": "$3",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$2",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$4",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            }

        ],
        "isRoot": true
    }
    """

    Given there are documents for the data source "data-source-name" in collection "documents"
      | uid | parent_uid | name          | description | type                                    |
      | 1   |            | package_1     |             | dmss://system/SIMOS/Package                    |
      | 2   | 1          | sub_package_1 |             | dmss://system/SIMOS/Package                    |
      | 3   | 1          | sub_package_2 |             | dmss://system/SIMOS/Package                    |
      | 4   | 2          | document_1    |             | dmss://system/SIMOS/Package                    |
      | 5   | 2          | document_2    |             | dmss://system/SIMOS/Blueprint                  |
      | 6   | 3          | container_1   |             | dmss://test-source-name/TestData/TestContainer |


    Given there exist document with id "7" in data source "data-source-name"
    """
    {
        "name": "document_3",
        "type": "dmss://test-source-name/TestData/ItemType"
    }
    """



  Scenario: Update complex list attribute
    Given i access the resource url "/api/documents/data-source-name/$7.complexList"
    When i make a form-data "POST" request
      """
      {
        "document":
       {
          "name": "item_1_contained",
          "type": "dmss://test-source-name/TestData/ItemTypeTwo",
          "extra": "extra_1"
        }
      }
      """
    Then the response status should be "OK"
    Given i access the resource url "/api/documents/data-source-name/$7.complexList"
    When i make a form-data "PUT" request
    """
    { "data":
    [
        {
          "name": "item_1_contained_modified",
          "type": "dmss://test-source-name/TestData/ItemTypeTwo",
          "extra": "extra_1_modified"
        }
    ]
    }
    """
    Then the response status should be "OK"
    And the response should be
    """
    {
      "data": [
          {
            "name": "item_1_contained_modified",
            "type": "dmss://test-source-name/TestData/ItemTypeTwo",
            "extra": "extra_1_modified"
          }
        ]
    }
    """
    Given i access the resource url "/api/documents/data-source-name/$7"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    {
      "_id": "7",
      "name": "document_3",
      "type": "dmss://test-source-name/TestData/ItemType",
      "complexList": [
          {
            "name": "item_1_contained_modified",
            "type": "dmss://test-source-name/TestData/ItemTypeTwo",
            "extra": "extra_1_modified"
          }
      ]
    }
    """
    Given i access the resource url "/api/documents/data-source-name/$7.complexList"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    [
          {
            "name": "item_1_contained_modified",
            "type": "dmss://test-source-name/TestData/ItemTypeTwo",
            "extra": "extra_1_modified"
          }
      ]
    """
    Given i access the resource url "/api/documents/data-source-name/$7.complexList[0]"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should be
    """
    {
      "name": "item_1_contained_modified",
      "type": "dmss://test-source-name/TestData/ItemTypeTwo",
      "extra": "extra_1_modified"
    }
    """


  Scenario: Update complex attribute
    Given i access the resource url "/api/documents/data-source-name/$7.complexList"
    When i make a form-data "POST" request
      """
      {
        "document":
       {
          "name": "item_1_contained",
          "type": "dmss://test-source-name/TestData/ItemTypeTwo",
          "extra": "extra_1",
          "complexAttribute": {
            "name": "itemForComplexAttribute",
            "type": "dmss://test-source-name/TestData/ItemTypeTwo",
            "extra": "extra_2"
          }
        }
      }
      """
    Given i access the resource url "/api/documents/data-source-name/$7.complexList[0].complexAttribute"
    When i make a form-data "PUT" request
    """
    { "data":
      {
        "name": "itemForComplexAttributeModified",
        "type": "dmss://test-source-name/TestData/ItemTypeTwo",
        "extra": "extra_2_modified"
      }
    }
    """

    Then the response status should be "OK"
    Given i access the resource url "/api/documents/data-source-name/$7.complexList[0]"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "item_1_contained",
      "type": "dmss://test-source-name/TestData/ItemTypeTwo",
      "extra": "extra_1",
      "complexAttribute": {
        "name": "itemForComplexAttributeModified",
        "type": "dmss://test-source-name/TestData/ItemTypeTwo",
        "extra": "extra_2_modified"
      }
    }
    """
    Given i access the resource url "/api/documents/data-source-name/$7.complexList[0].complexAttribute"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "itemForComplexAttributeModified",
      "type": "dmss://test-source-name/TestData/ItemTypeTwo",
      "extra": "extra_2_modified"
    }
    """

  Scenario: Validation errors if the address pointing to something that does not match the data type
    Given there exist document with id "10" in data source "test-source-name"
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

    Given there exist document with id "Company" in data source "test-source-name"
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
          "attributeType": "dmss://test-source-name/TestReplace/Person",
          "dimensions": "*",
          "label": "Employees"
        },
        {
          "name": "ceo",
          "type": "CORE:BlueprintAttribute",
          "attributeType": "dmss://test-source-name/TestReplace/Person",
          "label": "CEO",
          "contained": false,
          "optional": false
        },
        {
          "name": "accountant",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "attributeType": "dmss://test-source-name/TestReplace/Person",
          "label": "Accountant",
          "contained": false,
          "optional": false
        }
      ]
    }
    """

    Given there exist document with id "Person" in data source "test-source-name"
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

    Given there exist document with id "companyEntity" in data source "test-source-name"
    """
    {
      "name": "myCompany",
      "type": "dmss://test-source-name/TestReplace/Company",
      "employees": [
        {
          "name": "Miranda",
          "type": "dmss://test-source-name/TestReplace/Person",
          "phoneNumber": 1337
        },
        {
          "name": "John",
          "type": "dmss://test-source-name/TestReplace/Person",
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

    Given i access the resource url "/api/documents/test-source-name/$companyEntity.employees[0]"
    When i make a form-data "PUT" request
    """
    {
      "data": {
        "name": "Miranda",
        "type": "dmss://test-source-name/TestReplace/Person",
        "phoneNumber": 13371
      }
    }
    """
    Then the response status should be "OK"

    Given i access the resource url "/api/documents/test-source-name/$companyEntity.employees[0]"
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
    Then the response status should be "Bad Request"
    And the response should be
    """
    {
    "status": 400,
    "type": "ValidationException",
    "message": "Can not update the document with address dmss://test-source-name/$companyEntity.employees[0], since the address is not pointing to a reference, but the data is a reference.",
    "debug": "Values are invalid for requested operation.",
    "data": null
    }
    """

    Given i access the resource url "/api/documents/test-source-name/$companyEntity.accountant"
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

    Given i access the resource url "/api/documents/test-source-name/$companyEntity.accountant"
    When i make a form-data "PUT" request
    """
    {
      "data": {
        "name": "Miranda",
        "type": "dmss://test-source-name/TestReplace/Person",
        "phoneNumber": 13371
      }
    }
    """
    Then the response status should be "Bad Request"
    And the response should be
    """
    {
    "status": 400,
    "type": "ValidationException",
    "message": "Can not update the document with address dmss://test-source-name/$companyEntity.accountant, since the the address is pointing to a reference, but the data is not a reference.",
    "debug": "Values are invalid for requested operation.",
    "data": null
    }
    """