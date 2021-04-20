Feature: Document 2

  Background: There are data sources in the system

    Given there are data sources
      |       name         |
      | data-source-name   |
      | test-source-name   |
      | system             |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name       | database | collection | type     | dataTypes    |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1      | local    | documents  | mongo-db | default      |
      | test-source-name | db   | 27017 | maf      | maf      | false | blob-repo  | local    | blob-data  | mongo-db | default,blob |
      | data-source-name | db   | 27017 | maf      | maf      | false | doc-repo   | local    | test       | mongo-db | default      |
      | system           | db   | 27017 | maf      | maf      | false | system     | local    | system     | mongo-db | default      |


    Given there exist document with id "2" in data source "test-source-name"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "ItemType",
      "description": "",
      "attributes": [
        {
          "attributeType": "string", "type": "system/SIMOS/BlueprintAttribute",
          "name": "name"
        },
        {
          "attributeType": "string", "type": "system/SIMOS/BlueprintAttribute",
          "optional": true,
          "default": "",
          "name": "description"
        },
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "type"
        },
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
      "attributes": [
        {
          "attributeType": "string", "type": "system/SIMOS/BlueprintAttribute",
          "name": "name"
        },
        {
          "attributeType": "string", "type": "system/SIMOS/BlueprintAttribute",
          "optional": true,
          "default": "",
          "name": "description"
        },
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "type"
        },
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
      "attributes": [
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "name"
        },
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "type"
        },
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "description"
        },
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
          "optional": false,
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
        "isRoot": true,
        "storageRecipes":[],
        "uiRecipes":[]
    }
    """

    Given data modelling tool templates are imported

    Given there are documents for the data source "data-source-name" in collection "documents"
      | uid | parent_uid | name          | description | type                                    |
      | 1   |            | package_1     |             | system/SIMOS/Package                    |
      | 2   | 1          | sub_package_1 |             | system/SIMOS/Package                    |
      | 3   | 1          | sub_package_2 |             | system/SIMOS/Package                    |
      | 4   | 2          | document_1    |             | system/SIMOS/Package                    |
      | 5   | 2          | document_2    |             | system/SIMOS/Blueprint                  |
      | 6   | 3          | container_1   |             | test-source-name/TestData/TestContainer |

  Scenario: Update document (only contained)
    Given i access the resource url "/api/v1/documents/data-source-name/1"
    When i make a "PUT" request
    """
    {
      "name": "package_1",
      "type": "system/SIMOS/Package",
      "description": "new description"
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "data": {
        "name": "package_1",
        "type": "system/SIMOS/Package",
        "description": "new description"
      }
    }
    """

  Scenario: Update document (both contained and not contained)
    Given i access the resource url "/api/v1/documents/data-source-name/6"
    When i make a "PUT" request
    """
    {
      "name": "new_name",
      "type": "test-source-name/TestData/TestContainer",
      "description": "some description",
      "itemContained": {
          "name": "item_contained",
          "type": "test-source-name/TestData/ItemType",
           "extra": "extra_1"
      },
      "itemsContained": [
        {
          "name": "item_1_contained",
          "type": "test-source-name/TestData/ItemType",
          "list": ["a", "b", "c"],
          "complexList": [
              {
                "name": "item_1_contained",
                "type": "test-source-name/TestData/ItemTypeTwo",
                "extra": "extra_1"
              }
            ]
        }
      ],
      "itemNotContained": {
          "name": "item_single",
          "type": "test-source-name/TestData/ItemType",
           "extra": "extra_1"
      },
      "itemsNotContained": [
        {
          "name": "item_1",
          "type": "test-source-name/TestData/ItemType",
          "list": ["a", "b"],
          "complexList": [
              {
                "name": "item_1",
                "type": "test-source-name/TestData/ItemTypeTwo",
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
        "type": "test-source-name/TestData/TestContainer",
        "description": "some description",
        "itemContained": {
          "name": "item_contained",
          "type": "test-source-name/TestData/ItemType",
           "extra": "extra_1"
        },
        "itemsContained": [
        {
            "name": "item_1_contained",
            "type": "test-source-name/TestData/ItemType",
            "list": ["a", "b", "c"],
            "complexList": [
                {
                  "name": "item_1_contained",
                  "type": "test-source-name/TestData/ItemTypeTwo",
                  "extra": "extra_1"
                }
              ]
          }
        ],
        "itemNotContained": {
            "name": "item_single",
            "type": "test-source-name/TestData/ItemType",
            "extra": "extra_1"
        },
        "itemsNotContained": [
          {
            "name": "item_1",
            "type": "test-source-name/TestData/ItemType",
            "list": ["a", "b"],
            "complexList": [
              {
                "name": "item_1",
                "type": "test-source-name/TestData/ItemTypeTwo",
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
    And data modelling tool templates are imported
    When i make a "PUT" request
    """
    {
      "name": "item_single",
      "type": "test-source-name/TestData/ItemType"
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "data": {
        "name": "item_single",
        "type": "test-source-name/TestData/ItemType"
      }
    }
    """
