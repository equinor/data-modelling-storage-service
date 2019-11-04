Feature: Index

  Background: There are data sources in the system

    Given there are mongodb data sources
      | host | port  | username | password | tls   | name             | database | collection | documentType | type     |
      | db   | 27017 | maf      | maf      | false | data-source-name | maf      | documents  | blueprints   | mongo-db |
      | db   | 27017 | maf      | maf      | false | system           | dmt      | system     | blueprints   | mongo-db |
      | db   | 27017 | maf      | maf      | false | test-source-name | dmt      | test       | blueprints   | mongo-db |

    Given there are documents for the data source "data-source-name" in collection "documents"
      | uid | parent_uid | name          | description | type                                    |
      | 1   |            | blueprints    |             | system/DMT/Package                      |
      | 2   | 1          | sub_package_1 |             | system/DMT/Package                      |
      | 3   | 2          | document_1    |             | system/SIMOS/Blueprint                  |
      | 4   | 1          | custom_1      |             | test-source-name/TestData/TestContainer |

    Given there exist document with id "1" in data source "test"
    """
    {
        "name": "TestData",
        "description": "",
        "type": "system/DMT/Package",
        "content": [
            {
                "_id": "3",
                "name": "TestContainer"
            },
            {
                "_id": "2",
                "name": "ItemType"
            }
        ],
        "dependencies": [],
        "isRoot": true,
        "storageRecipes": [],
        "applications": []
    }
    """

    Given there exist document with id "2" in data source "test"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "ItemType",
      "description": "",
      "attributes": [
        {
          "type": "string",
          "name": "name"
        },
        {
          "type": "string",
          "name": "description"
        },
        {
          "type": "string",
          "name": "extra"
        }
      ]
    }
    """

    Given there exist document with id "3" in data source "test"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "TestContainer",
      "description": "",
      "attributes": [
        {
          "type": "string",
          "name": "name"
        },
        {
          "type": "string",
          "name": "description"
        },
        {
          "type": "test-source-name/TestData/ItemType",
          "name": "itemNotContainedInStorage"
        },
        {
          "type": "test-source-name/TestData/ItemType",
          "dimensions": "*",
          "name": "itemsNotContainedInStorage"
        },
        {
          "type": "test-source-name/TestData/ItemType",
          "name": "itemNotContainedInUi"
        },
        {
          "type": "test-source-name/TestData/ItemType",
          "dimensions": "*",
          "name": "itemsNotContainedInUi"
        }
      ],
      "storageRecipes": [
        {
          "name": "DefaultStorageRecipe",
          "type": "system/SIMOS/StorageRecipe",
          "description": "",
          "attributes": [
            {
              "name": "itemNotContainedInStorage",
              "contained": false
            },
            {
              "name": "itemsNotContainedInStorage",
              "contained": false
            }
          ]
        }
      ],
      "uiRecipes": [
        {
          "type": "system/SIMOS/UiRecipe",
          "name": "EDIT",
          "description": "",
          "attributes": [
            {
              "name": "itemNotContainedInUi",
              "contained": false
            },
            {
              "name": "itemsNotContainedInUi",
              "contained": false
            }
          ]
        }
      ]
    }
    """

  Scenario: Get index for single document (Root Package)
    Given I access the resource url "/api/v3/index/data-source-name/1"
    And data modelling tool templates are imported
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
       "1":{
          "parentId": null,
          "filename":"blueprints",
          "title":"blueprints",
          "id":"1",
          "nodeType":"document-node",
          "children":["2"],
          "type":"system/DMT/Package"
       }
    }
    """

  Scenario: Get index for single document (Package)
    Given I access the resource url "/api/v3/index/data-source-name/2"
    And data modelling tool templates are imported
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
       "2":{
          "filename":"sub_package_1",
          "title":"sub_package_1",
          "id":"2",
          "nodeType":"document-node",
          "children":[],
          "type":"system/DMT/Package"
       }
    }
    """

  Scenario: Get index for single document (Document)
    Given I access the resource url "/api/v3/index/data-source-name/3"
    And data modelling tool templates are imported
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
       "3":{
          "parentId": null,
          "filename":"document_1",
          "title":"document_1",
          "id":"3",
          "nodeType":"document-node",
          "children":[],
          "type":"system/SIMOS/Blueprint"
       }
    }
    """

  Scenario: Get index for single document (Custom Document)
    Given I access the resource url "/api/v3/index/data-source-name/4"
    And data modelling tool templates are imported
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
       "4":{
         "parentId": null,
         "filename":"custom_1",
         "title":"custom_1",
         "id":"4",
         "nodeType":"document-node",
         "children":[
           "4.itemNotContainedInUi_itemNotContainedInUi",
           "4_itemsNotContainedInUi"
         ],
         "type":"test-source-name/TestData/TestContainer"
       },
       "4.itemNotContainedInUi_itemNotContainedInUi": {
         "children": [],
         "filename": "itemNotContainedInUi",
         "id": "4.itemNotContainedInUi_itemNotContainedInUi",
         "nodeType": "document-node",
         "parentId": "4",
         "title": "itemNotContainedInUi",
         "type": "test-source-name/TestData/ItemType"
      },
      "4_itemsNotContainedInUi": {
         "children": [],
         "filename": "itemsNotContainedInUi",
         "id": "4_itemsNotContainedInUi",
         "nodeType": "document-node",
         "parentId": "4",
         "title": "itemsNotContainedInUi",
         "type": "test-source-name/TestData/TestContainer"
      }
    }
    """


