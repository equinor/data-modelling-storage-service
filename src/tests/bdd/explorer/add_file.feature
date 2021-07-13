Feature: Explorer - Add file

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
                "_id": "2",
                "name": "MultiplePdfContainer",
                "type": "system/SIMOS/Blueprint"
            },
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
                "_id": "6",
                "name": "parentEntity",
                "type": "data-source-name/root_package/Parent"
            },
            {
                "_id": "7",
                "name": "Hobby",
                "type": "system/SIMOS/Blueprint"
            },
            {
                "_id": "8",
                "name": "parentEntity2",
                "type": "data-source-name/root_package/Parent"
            }
        ]
    }
    """
    Given there exist document with id "2" in data source "data-source-name"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "MultiplePdfContainer",
      "description": "A recursive blueprint with multiple PDFs",
      "attributes": [
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "name"
        },
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "description"
        },
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "type",
          "default": "blueprints/root_package/RecursiveBlueprint"
        },
        {
          "name": "a_pdf",
          "attributeType": "system/SIMOS/blob_types/PDF",
          "type": "system/SIMOS/BlueprintAttribute"
        },
        {
          "name": "another_pdf",
          "attributeType": "system/SIMOS/blob_types/PDF",
          "type": "system/SIMOS/BlueprintAttribute"
        },
        {
          "name": "pdf_container",
          "attributeType": "data-source-name/root_package/MultiplePdfContainer",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true
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
        "type": "system/SIMOS/BlueprintAttribute",
        "optional": true
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


  Given there exist document with id "6" in data source "data-source-name"
    """
    {
      "type": "data-source-name/root_package/Parent",
      "name": "parentEntity",
      "description": "",
      "SomeChild": {}
    }
    """

  Given there exist document with id "7" in data source "data-source-name"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "Hobby",
      "description": "",
      "extends": ["system/SIMOS/NamedEntity"],
      "attributes": [
        {
        "name": "difficulty",
        "attributeType": "string",
        "type": "system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """

  Given there exist document with id "8" in data source "data-source-name"
    """
    {
      "type": "data-source-name/root_package/Parent",
      "name": "parentEntity2",
      "description": "",
      "SomeChild": {}
    }
    """



  Scenario: Add file - attribute for parentEntity
    Given i access the resource url "/api/v1/explorer/data-source-name/add-to-parent"
    When i make a "POST" request
    """
    {
      "name": "baseChildInParentEntity",
      "parentId": "6",
      "type": "data-source-name/root_package/BaseChild",
      "attribute": "SomeChild",
      "description": "base child in parent",
      "AValue": 0
    }
    """
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/data-source-name/6"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
    "document":
      {
          "_id": "6",
          "name": "parentEntity",
          "type": "data-source-name/root_package/Parent",
          "description": "",
          "SomeChild":
          {
            "name": "baseChildInParentEntity",
            "type": "data-source-name/root_package/BaseChild",
            "description": "base child in parent",
            "AValue": 0
          }
      }
    }
    """

  Scenario: Add file with wrong subtype to parent entity
    Given i access the resource url "/api/v1/explorer/data-source-name/add-to-parent"
    When i make a "POST" request
    """
    {
      "name": "hobbynumber1",
      "parentId": "8",
      "type": "data-source-name/root_package/Hobby",
      "attribute": "SomeChild",
      "description": "example hobby",
      "difficulty": "high"
    }
    """
    Then the response status should be "System Error"
    Given I access the resource url "/api/v1/documents/data-source-name/8"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
    "document":
      {
          "_id": "8",
          "name": "parentEntity2",
          "type": "data-source-name/root_package/Parent",
          "description": "",
          "SomeChild": {}
      }
    }
    """

   Scenario: Add file - not contained
    Given i access the resource url "/api/v1/explorer/data-source-name/add-to-parent"
    When i make a "POST" request
    """
    {
      "name": "new_document",
      "parentId": "1",
      "type": "system/SIMOS/Blueprint",
      "attribute": "content"
    }
    """
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/data-source-name/1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
       "blueprint":{
          "name":"Package",
          "type":"system/SIMOS/Blueprint"
       },
       "document":{
          "name":"root_package",
          "type":"system/SIMOS/Package",
          "content":[
            {
              "name": "MultiplePdfContainer"
            },
            {
              "name":"BaseChild"
            },
            {
              "name":"Parent"
            },
            {
              "name":"SpecialChild"
            },
            {
              "name": "parentEntity"
            },
            {
              "name":"Hobby"
            },
            {
              "name": "parentEntity2"
            },
            {
              "name": "new_document"
            }
          ],
          "isRoot":true
       }
    }
    """


  @skip
  Scenario: Add file with missing parameter name should fail
    Given i access the resource url "/api/v1/explorer/data-source-name/add-to-parent"
    When i make a "POST" request
    """
    {
      "parentId": "1",
      "type": "system/SIMOS/Blueprint"
    }
    """
    Then the response status should be "Bad Request"
    And the response should equal
    """
    {"type": "PARAMETERS_ERROR", "message": "name: is missing\nattribute: is missing"}
    """

  @skip
  Scenario: Add file with missing parameters should fail
    Given i access the resource url "/api/v1/explorer/data-source-name/add-to-parent"
    When i make a "POST" request
    """
    {}
    """
    Then the response status should be "Bad Request"
    And the response should equal
    """
    {
      "type": "PARAMETERS_ERROR",
      "message": "parentId: is missing\nname: is missing\ntype: is missing\nattribute: is missing"
    }
    """

  Scenario: Add file to parent that does not exists
    Given i access the resource url "/api/v1/explorer/data-source-name/add-to-parent"
    When i make a "POST" request
    """
    {
      "name": "new_document",
      "parentId": "-1",
      "type": "system/SIMOS/Blueprint",
      "attribute": "documents"
    }
    """
    Then the response status should be "Not Found"
    And the response should equal
    """
    {"type": "RESOURCE_ERROR", "message": "EntityNotFoundException: Document with id '-1' was not found in the 'data-source-name' data-source"}
    """

  Scenario: Add file with multiple PDFs
    Given i access the resource url "/api/v1/explorer/data-source-name/add-to-path"
    When i make a "POST" request with "4" files
    """
    {
      "directory": "/root_package/",
      "document": {
        "name": "new_pdf_container",
        "type": "data-source-name/root_package/MultiplePdfContainer",
        "description": "",
        "a_pdf": {
          "name": "MyPDF1",
          "description": "",
          "type": "system/SIMOS/blob_types/PDF",
          "blob_reference": "file1",
          "author": "Stig Oskar"
        },
        "another_pdf": {
          "name": "MyPDF2",
          "description": "",
          "type": "system/SIMOS/blob_types/PDF",
          "blob_reference": "file2",
          "author": "Stig Oskar"
        },
        "pdf_container": {
          "name": "second_pdf_container",
          "type": "data-source-name/root_package/MultiplePdfContainer",
          "description": "",
          "a_pdf": {
            "name": "MyPDF3",
            "description": "",
            "type": "system/SIMOS/blob_types/PDF",
            "blob_reference": "file3",
            "author": "Stig Oskar"
          },
          "another_pdf": {
            "name": "MyPDF4",
            "description": "",
            "type": "system/SIMOS/blob_types/PDF",
            "blob_reference": "file4",
            "author": "Stig Oskar"
          },
          "pdf_container": {}
        }
      }
    }
    """
    Then the response status should be "OK"