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
      "type": "sys://system/SIMOS/Blueprint",
      "name": "ItemType",
      "description": "",
      "extends": ["sys://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "attributeType": "string",
          "type": "sys://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "extra"
        },
        {
          "attributeType": "string",
          "type": "sys://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "list"
        },
        {
          "attributeType": "sys://test-source-name/TestData/ItemTypeTwo",
          "type": "sys://system/SIMOS/BlueprintAttribute",
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
      "type": "sys://system/SIMOS/Blueprint",
      "name": "ItemTypeTwo",
      "description": "",
      "extends": ["sys://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "attributeType": "string",
          "type": "sys://system/SIMOS/BlueprintAttribute",
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
      "type": "sys://system/SIMOS/Blueprint",
      "name": "TestContainer",
      "description": "",
      "extends": ["sys://system/SIMOS/NamedEntity"],
      "attributes": [
        {
          "attributeType": "sys://test-source-name/TestData/ItemType",
          "type": "sys://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "itemContained"
        },
        {
          "attributeType": "sys://test-source-name/TestData/ItemType",
          "type": "sys://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "dimensions": "*",
          "name": "itemsContained"
        },
        {
          "attributeType": "sys://test-source-name/TestData/ItemType",
          "type": "sys://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "name": "itemNotContained"
        },
        {
          "attributeType": "sys://test-source-name/TestData/ItemType",
          "type": "sys://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "dimensions": "*",
          "name": "itemsNotContained"
        }
      ],
      "storageRecipes": [
        {
          "name": "DefaultStorageRecipe",
          "type": "sys://system/SIMOS/StorageRecipe",
          "description": "",
          "attributes": [
            {
              "name": "itemNotContained",
              "type": "sys://test-source-name/TestData/ItemType",
              "contained": false,
              "storageTypeAffinity": "blob"
            },
            {
              "name": "itemsNotContained",
              "type": "sys://test-source-name/TestData/ItemType",
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
        "type": "sys://system/SIMOS/Package",
        "content": [
            {
                "_id": "3",
                "name": "TestContainer",
                "type": "sys://test-source-name/TestData/TestContainer"
            },
            {
                "_id": "2",
                "name": "ItemType",
                "type": "sys://test-source-name/TestData/ItemType"
            },
            {
                "_id": "4",
                "name": "ItemTypeTwo",
                "type": "sys://test-source-name/TestData/ItemTypeTwo"
            }

        ],
        "isRoot": true,
        "storageRecipes":[],
        "uiRecipes":[]
    }
    """

    Given there are documents for the data source "data-source-name" in collection "documents"
      | uid | parent_uid | name          | description | type                                    |
      | 1   |            | package_1     |             | sys://system/SIMOS/Package                    |
      | 2   | 1          | sub_package_1 |             | sys://system/SIMOS/Package                    |
      | 3   | 1          | sub_package_2 |             | sys://system/SIMOS/Package                    |
      | 4   | 2          | document_1    |             | sys://system/SIMOS/Package                    |
      | 5   | 2          | document_2    |             | sys://system/SIMOS/Blueprint                  |
      | 6   | 3          | container_1   |             | sys://test-source-name/TestData/TestContainer |

  Scenario: Update document (only contained)
    Given i access the resource url "/api/v1/documents/data-source-name/1"
    When i make a form-data "PUT" request
    """
    {
      "name": "package_1",
      "type": "sys://system/SIMOS/Package",
      "description": "new description",
      "isRoot": true
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "data": {
        "name": "package_1",
        "type": "sys://system/SIMOS/Package",
        "description": "new description",
        "isRoot": true
      }
    }
    """

  Scenario: Update document (both contained and not contained)
    Given i access the resource url "/api/v1/documents/data-source-name/6"
    When i make a form-data "PUT" request
    """
    {
      "name": "new_name",
      "type": "sys://test-source-name/TestData/TestContainer",
      "description": "some description",
      "itemContained": {
          "name": "item_contained",
          "type": "sys://test-source-name/TestData/ItemType",
           "extra": "extra_1"
      },
      "itemsContained": [
        {
          "name": "item_1_contained",
          "type": "sys://test-source-name/TestData/ItemType",
          "list": ["a", "b", "c"],
          "complexList": [
              {
                "name": "item_1_contained",
                "type": "sys://test-source-name/TestData/ItemTypeTwo",
                "extra": "extra_1"
              }
            ]
        }
      ],
      "itemNotContained": {
          "name": "item_single",
          "type": "sys://test-source-name/TestData/ItemType",
           "extra": "extra_1"
      },
      "itemsNotContained": [
        {
          "name": "item_1",
          "type": "sys://test-source-name/TestData/ItemType",
          "list": ["a", "b"],
          "complexList": [
              {
                "name": "item_1",
                "type": "sys://test-source-name/TestData/ItemTypeTwo",
                "extra": "extra_1"
              }
            ]
        }
      ]
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "data": {
        "name": "new_name",
        "type": "sys://test-source-name/TestData/TestContainer",
        "description": "some description",
        "itemContained": {
          "name": "item_contained",
          "type": "sys://test-source-name/TestData/ItemType",
           "extra": "extra_1"
        },
        "itemsContained": [
        {
            "name": "item_1_contained",
            "type": "sys://test-source-name/TestData/ItemType",
            "list": ["a", "b", "c"],
            "complexList": [
                {
                  "name": "item_1_contained",
                  "type": "sys://test-source-name/TestData/ItemTypeTwo",
                  "extra": "extra_1"
                }
              ]
          }
        ],
        "itemNotContained": {
            "name": "item_single",
            "type": "sys://test-source-name/TestData/ItemType",
            "extra": "extra_1"
        },
        "itemsNotContained": [
          {
            "name": "item_1",
            "type": "sys://test-source-name/TestData/ItemType",
            "list": ["a", "b"],
            "complexList": [
              {
                "name": "item_1",
                "type": "sys://test-source-name/TestData/ItemTypeTwo",
                "extra": "extra_1"
              }
            ]
          }
        ]
      }
    }
    """

  Scenario: Update document (attribute and not contained)
    Given i access the resource url "/api/v1/documents/data-source-name/6?attribute=itemNotContained"
    When i make a form-data "PUT" request
    """
    {
      "name": "item_single",
      "type": "sys://test-source-name/TestData/ItemType"
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "data": {
        "name": "item_single",
        "type": "sys://test-source-name/TestData/ItemType"
      }
    }
    """
