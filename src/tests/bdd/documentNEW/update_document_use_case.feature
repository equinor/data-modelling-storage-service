Feature: Update document

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
        "isRoot": true,
        "storageRecipes":[],
        "uiRecipes":[]
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

  Scenario: Update document (only contained)
    Given i access the resource url "/api/v1/documents/data-source-name/1"
    When i make a form-data "PUT" request
    """
    {
      "name": "package_1",
      "type": "system/SIMOS/Package",
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
        "type": "system/SIMOS/Package",
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
    When i make a form-data "PUT" request
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


Feature: Update document that has blob data

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available

    Given there are data sources
      | name    |
      | test-DS |

    Given there are repositories in the data sources
      | data-source | host | port  | username | password | tls   | name       | database | collection | type     | dataTypes |
      | test-DS     | db   | 27017 | maf      | maf      | false | documents  | bdd-test | documents  | mongo-db | default   |
      | test-DS     | db   | 27017 | maf      | maf      | false | blob-repo  | bdd-test | blob-data  | mongo-db | blob      |


 Given there exist document with id "1" in data source "test-DS"
    """
    {
        "name": "root_package",
        "description": "",
        "type": "system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
                "_id": "2",
                "name": "MultiplePdfContainer",
                "type": "system/SIMOS/Blueprint"
            },
            {
                "_id": "3",
                "name": "new_pdf_container",
                "type": "test-DS/root_package/MultiplePdfContainer"
            }
        ]
    }
    """
    Given there exist document with id "2" in data source "test-DS"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "MultiplePdfContainer",
      "extends": ["system/SIMOS/DefaultUiRecipes","system/SIMOS/NamedEntity"],
      "description": "A recursive blueprint with multiple PDFs",
      "attributes": [
        {
          "name": "a_pdf",
          "attributeType": "system/SIMOS/blob_types/PDF",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true
        },
        {
          "name": "another_pdf",
          "attributeType": "system/SIMOS/blob_types/PDF",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true
        },
        {
          "name": "pdf_container",
          "attributeType": "test-DS/root_package/MultiplePdfContainer",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true
        }
      ]
    }
    """
    Given there exist document with id "3" in data source "test-DS"
    """
    {
        "name": "new_pdf_container",
        "type": "test-DS/root_package/MultiplePdfContainer",
        "a_pdf": {},
        "another_pdf": {},
        "pdf_container": {}
    }
    """

  Scenario: Update document with multiple blob entities
    Given i access the resource url "/api/v1/documents/test-DS/3"
    When i make a "PUT" request with "4" files
    """
    {"data":{
        "name": "new_pdf_container",
        "type": "test-DS/root_package/MultiplePdfContainer",
        "a_pdf": {
          "name": "MyPDF1",
          "description": "",
          "type": "system/SIMOS/blob_types/PDF",
          "blob": {
            "name": "file1",
            "type": "system/SIMOS/Blob",
            "size": 0
          },
          "author": "Stig Oskar"
        },
        "another_pdf": {
          "name": "MyPDF2",
          "description": "",
          "type": "system/SIMOS/blob_types/PDF",
          "blob": {
            "name": "file2",
            "type": "system/SIMOS/Blob",
            "_blob_id": "",
            "size": 0
          },
          "author": "Stig Oskar"
        },
        "pdf_container": {
          "name": "second_pdf_container",
          "type": "test-DS/root_package/MultiplePdfContainer",
          "description": "",
          "a_pdf": {
            "name": "MyPDF3",
            "description": "",
            "type": "system/SIMOS/blob_types/PDF",
            "blob": {
              "name": "file3",
              "type": "system/SIMOS/Blob",
              "_blob_id": "",
              "size": 0
            },
            "author": "Stig Oskar"
          },
          "another_pdf": {
            "name": "MyPDF4",
            "description": "",
            "type": "system/SIMOS/blob_types/PDF",
            "blob": {
              "name": "file4",
              "type": "system/SIMOS/Blob",
              "_blob_id": "",
              "size": 0
            },
            "author": "Stig Oskar"
          },
          "pdf_container": {}
        }
    }}
    """
    Then the response status should be "OK"

