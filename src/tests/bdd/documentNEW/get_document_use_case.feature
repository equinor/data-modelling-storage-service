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
      "type": "system/SIMOS/Blueprint",
      "name": "ItemType",
      "description": "",
      "extends": ["system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "extra"
        },
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "list"
        },
        {
          "attributeType": "test-source-name/TestData/ItemTypeTwo",
          "type": "system/SIMOS/BlueprintAttribute",
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
      "type": "system/SIMOS/Blueprint",
      "name": "ItemTypeTwo",
      "description": "",
      "extends": ["system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
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
      "type": "system/SIMOS/Blueprint",
      "name": "TestContainer",
      "description": "",
      "extends": ["system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "attributeType": "test-source-name/TestData/ItemType",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "itemContained"
        },
        {
          "attributeType": "test-source-name/TestData/ItemType",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true,
          "dimensions": "*",
          "name": "itemsContained"
        },
        {
          "attributeType": "test-source-name/TestData/ItemType",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "itemNotContained"
        },
        {
          "attributeType": "test-source-name/TestData/ItemType",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true,
          "dimensions": "*",
          "name": "itemsNotContained"
        }
      ],
      "storageRecipes": [
        {
          "name": "DefaultStorageRecipe",
          "type": "system/SIMOS/StorageRecipe",
          "description": "",
          "attributes": [
            {
              "name": "itemNotContained",
              "type": "test-source-name/TestData/ItemType",
              "contained": false,
              "storageTypeAffinity": "blob"
            },
            {
              "name": "itemsNotContained",
              "type": "test-source-name/TestData/ItemType",
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
        "type": "system/SIMOS/Package",
        "content": [
            {
                "_id": "3",
                "name": "TestContainer",
                "type": "test-source-name/TestData/TestContainer"
            },
            {
                "_id": "2",
                "name": "ItemType",
                "type": "test-source-name/TestData/ItemType"
            },
            {
                "_id": "4",
                "name": "ItemTypeTwo",
                "type": "test-source-name/TestData/ItemTypeTwo"
            }

        ],
        "isRoot": true
    }
    """

    Given there are documents for the data source "data-source-name" in collection "documents"
      | uid | parent_uid | name          | description | type                                    |
      | 1   |            | package_1     |             | system/SIMOS/Package                    |
      | 2   | 1          | sub_package_1 |             | system/SIMOS/Package                    |
      | 3   | 1          | sub_package_2 |             | system/SIMOS/Package                    |
      | 4   | 2          | document_1    |             | system/SIMOS/Package                    |
      | 5   | 2          | document_2    |             | system/SIMOS/Blueprint                  |
      | 6   | 3          | container_1   |             | test-source-name/TestData/TestContainer |

  Scenario: Get document by id
    Given I access the resource url "/api/v1/documents/data-source-name/1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name":"package_1",
      "type":"system/SIMOS/Package",
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
    Given I access the resource url "/api/v1/documents-by-path/data-source-name?path=package_1/sub_package_1/document_1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "_id": "4",
      "name": "document_1",
      "type": "system/SIMOS/Package",
      "isRoot": false,
      "content": []
    }
    """

  Scenario: Get attribute
    Given I access the resource url "/api/v1/documents/test-source-name/1?attribute=content.0"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "TestContainer"
    }
    """

Feature: Get document with subtypes
  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      | name             |
      | data-source-name |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name      | database | collection | type     | dataTypes |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1     |  bdd-test    | documents  | mongo-db | default   |
      | data-source-name | db   | 27017 | maf      | maf      | false | blob-repo |  bdd-test    | test       | mongo-db | blob      |


    Given there exist document with id "1" in data source "data-source-name"
    """
    {
        "name": "root_package",
        "description": "",
        "type": "system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
                "_id": "3",
                "name": "BaseChild",
                "type": "system/SIMOS/Blueprint"
            },
            {
                "_id": "4",
                "name": "Parent",
                "type": "system/SIMOS/Blueprint"
            },
            {
                "_id": "5",
                "name": "SpecialChild",
                "type": "system/SIMOS/Blueprint"
            },
            {
                "_id": "7",
                "name": "parentEntity",
                "type": "data-source-name/root_package/Parent"
            }
        ]
    }
    """

    Given there exist document with id "3" in data source "data-source-name"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "BaseChild",
      "description": "",
      "extends": ["system/SIMOS/NamedEntity"],
      "attributes": [
        {
        "name": "AValue",
        "attributeType": "integer",
        "type": "system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """


    Given there exist document with id "4" in data source "data-source-name"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "Parent",
      "description": "",
      "extends": ["system/SIMOS/NamedEntity"],
      "attributes": [
        {
        "name": "SomeChild",
        "attributeType": "data-source-name/root_package/BaseChild",
        "type": "system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """

    Given there exist document with id "5" in data source "data-source-name"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "SpecialChild",
      "description": "",
      "extends": ["data-source-name/root_package/BaseChild"],
      "attributes": [
        {
          "name": "AnExtraValue",
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """




  Given there exist document with id "7" in data source "data-source-name"
    """
    {
      "type": "data-source-name/root_package/Parent",
      "name": "parentEntity",
      "description": "",
      "SomeChild": {
        "name": "specialChildInParent2",
        "type": "data-source-name/root_package/SpecialChild",
        "description": "special child type",
        "AValue": 222,
        "AnExtraValue": "extra value"
      }
    }
    """

  Given there exist document with id "8" in data source "data-source-name"
    """
    {
      "type": "data-source-name/root_package/Parent",
      "name": "parentEntity2",
      "description": "",
      "SomeChild": {
        "name": "baseChildInParent",
        "type": "data-source-name/root_package/BaseChild",
        "description": "base child type",
        "AValue": 333
      }
    }
    """

  Scenario: fetch entity with a subtype attribute
    Given i access the resource url "/api/v1/documents/data-source-name/7"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
       "_id": "7",
       "name": "parentEntity",
       "type": "data-source-name/root_package/Parent",
       "description": "",
       "SomeChild":
        {
          "name": "specialChildInParent2",
          "type": "data-source-name/root_package/SpecialChild",
          "description": "special child type",
          "AValue": 222,
          "AnExtraValue": "extra value"
        }
    }
    """


  Scenario: fetch entity with original attribute type
    Given i access the resource url "/api/v1/documents/data-source-name/8"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
       "_id": "8",
       "name": "parentEntity2",
       "type": "data-source-name/root_package/Parent",
       "description": "",
       "SomeChild":
        {
          "name": "baseChildInParent",
          "type": "data-source-name/root_package/BaseChild",
          "description": "base child type",
          "AValue": 333
        }
    }
    """
