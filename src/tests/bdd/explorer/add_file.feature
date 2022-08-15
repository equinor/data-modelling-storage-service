Feature: Explorer - Add file

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      | name             |
      | test-DS |

    Given there are repositories in the data sources
      | data-source | host | port  | username | password | tls   | name      | database  | collection | type     | dataTypes |
      | test-DS     | db   | 27017 | maf      | maf      | false | repo1     |  bdd-test | documents  | mongo-db | default   |
      | test-DS     | db   | 27017 | maf      | maf      | false | blob-repo |  bdd-test | test       | mongo-db | blob      |


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
                "type": "test-DS/root_package/Parent"
            },
            {
                "_id": "7",
                "name": "Hobby",
                "type": "system/SIMOS/Blueprint"
            },
            {
                "_id": "8",
                "name": "Comment",
                "type": "system/SIMOS/Blueprint"
            }
        ]
    }
    """
    Given there exist document with id "2" in data source "test-DS"
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


    Given there exist document with id "4" in data source "test-DS"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "Parent",
      "description": "",
      "extends": ["system/SIMOS/NamedEntity"],
      "attributes": [
        {
        "name": "SomeChild",
        "attributeType": "test-DS/root_package/BaseChild",
        "type": "system/SIMOS/BlueprintAttribute",
        "optional": true
        }
      ]
    }
    """

    Given there exist document with id "5" in data source "test-DS"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "SpecialChild",
      "description": "",
      "extends": ["test-DS/root_package/BaseChild"],
      "attributes": [
        {
          "name": "AnExtraValue",
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute"
        },
        {
          "name": "Hobbies",
          "attributeType": "test-DS/root_package/Hobby",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true,
          "dimensions": "*"
        }
      ]
    }
    """


  Given there exist document with id "6" in data source "test-DS"
    """
    {
      "type": "test-DS/root_package/Parent",
      "name": "parentEntity",
      "description": "",
      "SomeChild": {}
    }
    """

  Given there exist document with id "7" in data source "test-DS"
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

  Given there exist document with id "8" in data source "test-DS"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "Comment",
      "description": "a comment blueprint, that does not require a name",
      "attributes": [
        {
        "name": "text",
        "attributeType": "string",
        "type": "system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """

  Scenario: Add file - attribute for parentEntity
    Given i access the resource url "/api/v1/explorer/test-DS/6.SomeChild"
    When i make a "POST" request
    """
    {
      "name": "baseChildInParentEntity",
      "type": "test-DS/root_package/BaseChild",
      "description": "base child in parent",
      "AValue": 0
    }
    """
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/test-DS/6"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
          "_id": "6",
          "name": "parentEntity",
          "type": "test-DS/root_package/Parent",
          "description": "",
          "SomeChild":
          {
            "name": "baseChildInParentEntity",
            "type": "test-DS/root_package/BaseChild",
            "description": "base child in parent",
            "AValue": 0
          }
    }
    """

  Scenario: Add file (rootPackage) to root of data_source
    Given i access the resource url "/api/v1/explorer/test-DS"
    When i make a "POST" request
    """
    {
      "name": "newRootPackage",
      "type": "system/SIMOS/Package",
      "isRoot": true,
      "content": []
    }
    """
    Then the response status should be "OK"

  Scenario: Add file with wrong subtype to parent entity
    Given i access the resource url "/api/v1/explorer/test-DS/6.SomeChild"
    When i make a "POST" request
    """
    {
      "name": "hobbynumber1",
      "type": "test-DS/root_package/Hobby",
      "description": "example hobby",
      "difficulty": "high"
    }
    """
    Then the response status should be "Bad Request"
    Given I access the resource url "/api/v1/documents/test-DS/6"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
          "_id": "6",
          "name": "parentEntity",
          "type": "test-DS/root_package/Parent",
          "description": "",
          "SomeChild": {}
    }
    """

  Scenario: Add file with an extended type to parent entity
    Given i access the resource url "/api/v1/explorer/test-DS/6.SomeChild"
    When i make a "POST" request
    """
    {
      "name": "specialChild",
      "type": "test-DS/root_package/SpecialChild",
      "description": "specialized child",
      "AValue": 39,
      "AnExtraValue": "abc",
      "Hobbies": [
        {
          "name": "Football",
          "type": "test-DS/root_package/Hobby",
          "description": "sport",
          "difficulty": "high"
        }
      ]
    }
    """
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/test-DS/6"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
          "_id": "6",
          "name": "parentEntity",
          "type": "test-DS/root_package/Parent",
          "description": "",
          "SomeChild":
          {
            "name": "specialChild",
            "type": "test-DS/root_package/SpecialChild",
            "description": "specialized child",
            "AValue": 39,
            "AnExtraValue": "abc"
          }
    }
    """

  Scenario: Add file - not contained
    Given i access the resource url "/api/v1/explorer/test-DS/1.content?update_uncontained=True"
    When i make a "POST" request
    """
    {
      "name": "new_document",
      "type": "system/SIMOS/Blueprint"
    }
    """
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/test-DS/1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
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
              "name":"Comment"
            },
            {
              "name": "new_document"
            }
          ],
          "isRoot":true
    }
    """

  Scenario: Add file with missing parameters should fail
    Given i access the resource url "/api/v1/explorer/test-DS/6.whatever"
    When i make a "POST" request
    """
    {}
    """
    Then the response status should be "Bad Request"
    And the response should be
    """
    BadRequestException: Every entity must have a 'type' attribute
    """

  Scenario: Add file to parent that does not exists
    Given i access the resource url "/api/v1/explorer/test-DS/-1.documents"
    When i make a "POST" request
    """
    {
      "name": "new_document",
      "type": "system/SIMOS/Blueprint"
    }
    """
    Then the response status should be "Not Found"
    And the response should be
    """
    EntityNotFoundException: Document with id '-1' was not found in the 'test-DS' data-source
    """

  Scenario: Add file to parent with missing permissions on parent
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "someoneElse",
      "others": "READ"
    }
    """
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    Given i access the resource url "/api/v1/explorer/test-DS/1.content"
    When i make a "POST" request
    """
    {
      "name": "new_document",
      "type": "system/SIMOS/Blueprint"
    }
    """
    Then the response status should be "Forbidden"
    And the response should be
    """
    MissingPrivilegeException: The requested operation requires 'WRITE' privileges
    """

  Scenario: Add file with duplicate name
    Given i access the resource url "/api/v1/explorer/test-DS/add-to-path?directory=/root_package/"
    When i make a "POST" request with "1" files
    """
      {
        "document": {
          "type": "test-DS/root_package/Parent",
          "name": "parentEntity",
          "description": "",
          "SomeChild": {}
        }
      }
    """
    Then the response status should be "Bad Request"
    And the response should be
    """
    DuplicateFileNameException: 'test-DS/root_package/parentEntity' already exists
    """


  Scenario: Add Comment entity without a name attribute with add-raw endpoint
    Given i access the resource url "/api/v1/explorer/test-DS/add-raw"
    When i make a "POST" request
    """
    {
        "_id": "429cb3da-ebbe-4ea6-80a6-b6bca0f67aaa",
        "type": "test-DS/root_package/Comment",
        "description": "comment entity with no name",
        "text": "example comment"
    }
    """
    Then the response status should be "OK"


  Scenario: Add Parent entity without a name attribute with add-to-path endpoint
    Given i access the resource url "/api/v1/explorer/test-DS/add-to-path?directory=/root_package/&update_uncontained=True"
    When i make a "POST" request with "1" files
    """
    {
      "document":
      {
        "type": "test-DS/root_package/Parent",
        "description": "parent entity with no name"
      }
    }
    """
    Then the response status should be "Unprocessable Entity"
    And the response should be
    """
    ValidationException: Required attribute 'name' not found in the entity
    """

  Scenario: Adding file with id set to empty string should generate new uid
    Given I access the resource url "/api/v1/explorer/test-DS/add-to-path?directory=/root_package/"
    When i make a "POST" request with "1" files
    """
    {
      "document": {
        "_id": "",
        "type":"system/SIMOS/Blueprint",
        "name": "new_bp",
        "description": "Blueprint with no name"
      }
    }
    """
    Then the response status should be "OK"
    And the response should have valid uid

  Scenario: Adding file with id
    Given I access the resource url "/api/v1/explorer/test-DS/add-to-path?directory=/root_package/"
    When i make a "POST" request with "1" files
    """
    {
      "document": {
        "_id": "2283c9b0-d509-46c9-a153-94c79f4d7b7b",
        "type":"system/SIMOS/Blueprint",
        "name": "new_bp",
        "description": "Blueprint with no name"
      }
    }
    """
    Then the response status should be "OK"
    And the response should have valid uid


  Scenario: Add Comment entity without a name attribute with add-to-path endpoint
    Given i access the resource url "/api/v1/explorer/test-DS/add-to-path?directory=/root_package/&update_uncontained=True"
    When i make a "POST" request with "1" files
    """
    {
      "document":
      {
        "type": "test-DS/root_package/Comment",
        "description": "comment entity with no name",
        "text": "example comment"
      }
    }
    """
    Then the response status should be "OK"

  Scenario: Add blueprint without a name attribute with add-to-path endpoint should fail
    Given i access the resource url "/api/v1/explorer/test-DS/add-to-path?directory=/root_package/&update_uncontained=True"
    When i make a "POST" request with "1" files
    """
    {
      "document":
      {
        "type":"system/SIMOS/Blueprint",
        "description": "Blueprint with no name"
      }
    }
    """
    Then the response status should be "Unprocessable Entity"
    And the response should be
    """
    ValidationException: Required attribute 'name' not found in the entity
    """

  Scenario: Add package without a name attribute with add-to-path endpoint should fail
    Given i access the resource url "/api/v1/explorer/test-DS/add-to-path?directory=/root_package/&update_uncontained=True"
    When i make a "POST" request with "1" files
    """
    {
      "document":
      {
        "type":"system/SIMOS/Package",
        "description": "Package with no name"
      }
    }
    """
    Then the response status should be "Unprocessable Entity"
    And the response should be
    """
    ValidationException: Required attribute 'name' not found in the entity
    """

  Scenario: Add parent entity without a name attribute with add_by_parent_id endpoint
    Given i access the resource url "/api/v1/explorer/test-DS/1.content?update_uncontained=True"
    When i make a "POST" request
    """
    {
      "type": "test-DS/root_package/Parent",
      "description": "parent entity with no name"
    }
    """
    Then the response status should be "Unprocessable Entity"
    And the response should be
    """
    ValidationException: Required attribute 'name' not found in the entity
    """

  Scenario: Add comment entity without a name attribute with add_by_parent_id endpoint
    Given i access the resource url "/api/v1/explorer/test-DS/1.content?update_uncontained=True"
    When i make a "POST" request
    """
    {
      "type": "test-DS/root_package/Comment",
      "description": "comment entity with no name",
      "text": "example comment"
    }
    """
    Then the response status should be "OK"

  Scenario: Add blueprint without a name using add_by_parent_id endpoint should fail
    Given i access the resource url "/api/v1/explorer/test-DS/1.content"
    When i make a "POST" request
    """
    {
      "type":"system/SIMOS/Blueprint",
      "description": "Blueprint with no name"
    }
    """
    Then the response status should be "Unprocessable Entity"
    And the response should be
    """
    ValidationException: Required attribute 'name' not found in the entity
    """

  Scenario: Add package without a name using add_by_parent_id endpoint should fail
    Given i access the resource url "/api/v1/explorer/test-DS/1.content"
    When i make a "POST" request
    """
    {
      "type":"system/SIMOS/Package",
      "description": "Package with no name"
    }
    """
    Then the response status should be "Unprocessable Entity"
    And the response should be
    """
    ValidationException: Required attribute 'name' not found in the entity
    """

  Scenario: Add file with multiple PDFs
    Given i access the resource url "/api/v1/explorer/test-DS/add-to-path?directory=/root_package/&update_uncontained=True"
    When i make a "POST" request with "4" files
    """
    {
      "document": {
        "name": "new_pdf_container",
        "type": "test-DS/root_package/MultiplePdfContainer",
        "description": "",
        "a_pdf": {
          "name": "MyPDF1",
          "description": "",
          "type": "system/SIMOS/blob_types/PDF",
          "blob": {
            "name": "file1",
            "type": "system/SIMOS/Blob",
            "_blob_id": ""
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
            "_blob_id": ""
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
              "_blob_id": ""
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
              "size": 0,
              "_blob_id": ""
            },
            "author": "Stig Oskar"
          },
          "pdf_container": {}
        }
      }
    }
    """
    Then the response status should be "OK"