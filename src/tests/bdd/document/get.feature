Feature: Get document

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      |       name         |
      | data-source-name   |
      | test-source-name   |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name       | database    | collection | type     | dataTypes    |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1      | bdd-test    | documents  | mongo-db | default      |
      | test-source-name | db   | 27017 | maf      | maf      | false | blob-repo  | bdd-test    | blob-data  | mongo-db | default,blob |
      | data-source-name | db   | 27017 | maf      | maf      | false | doc-repo   | bdd-test    | test       | mongo-db | default      |

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
          "name": "list"
        },
        {
          "attributeType": "dmss://test-source-name/TestData/ItemTypeTwo",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "complexList",
          "dimensions" : "*"
        }
      ],
      "storageRecipes":[],
      "uiRecipes":[]
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
        }
      ],
      "storageRecipes":[],
      "uiRecipes":[]
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
      ],
      "storageRecipes": [
        {
          "name": "DefaultStorageRecipe",
          "type": "dmss://system/SIMOS/StorageRecipe",
          "description": "",
          "attributes": [
            {
              "name": "itemNotContained",
              "type": "dmss://test-source-name/TestData/ItemType",
              "contained": false,
              "storageTypeAffinity": "blob"
            },
            {
              "name": "itemsNotContained",
              "type": "dmss://test-source-name/TestData/ItemType",
              "contained": false
            }
          ]
        }
      ],
      "uiRecipes":[]
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

  Scenario: Get document by id
    Given I access the resource url "/api/documents/data-source-name/$1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name":"package_1",
      "type":"dmss://system/SIMOS/Package",
      "content":[
         {
            "name":"sub_package_1"
         },
         {
            "name":"sub_package_2"
         }
      ],
      "isRoot":true
    }
    """

  Scenario: Get document by path
    Given I access the resource url "/api/documents/dmss://data-source-name/package_1/sub_package_1/document_1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "_id": "4",
      "name": "document_1",
      "type": "dmss://system/SIMOS/Package",
      "isRoot": false,
      "content": []
    }
    """

  Scenario: Get attribute
    Given I access the resource url "/api/documents/test-source-name/$1.content[0]"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "TestContainer"
    }
    """
