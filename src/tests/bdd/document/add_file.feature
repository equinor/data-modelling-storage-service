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
        "type": "dmss://system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
                "address": "$2",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$3",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$4",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$5",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$6",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$7",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            },
            {
                "address": "$8",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "link"
            }
        ]
    }
    """
    Given there exist document with id "2" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "MultiplePdfContainer",
      "description": "A recursive blueprint with multiple PDFs",
      "attributes": [
        {
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "name"
        },
        {
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "description"
        },
        {
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "type",
          "default": "blueprints/root_package/RecursiveBlueprint"
        },
        {
          "name": "a_pdf",
          "attributeType": "dmss://system/SIMOS/PDF",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        },
        {
          "name": "another_pdf",
          "attributeType": "dmss://system/SIMOS/PDF",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        },
        {
          "name": "pdf_container",
          "attributeType": "dmss://test-DS/root_package/MultiplePdfContainer",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true
        }
      ]
    }
    """

    Given there exist document with id "3" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "BaseChild",
      "description": "",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
        "name": "AValue",
        "attributeType": "integer",
        "type": "dmss://system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """


    Given there exist document with id "4" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "Parent",
      "description": "",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
        "name": "SomeChild",
        "attributeType": "dmss://test-DS/root_package/BaseChild",
        "type": "dmss://system/SIMOS/BlueprintAttribute",
        "optional": true
        }
      ]
    }
    """

    Given there exist document with id "5" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "SpecialChild",
      "description": "",
      "extends": ["dmss://test-DS/root_package/BaseChild"],
      "attributes": [
        {
          "name": "AnExtraValue",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        },
        {
          "name": "Hobbies",
          "attributeType": "dmss://test-DS/root_package/Hobby",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true,
          "dimensions": "*"
        }
      ]
    }
    """


  Given there exist document with id "6" in data source "test-DS"
    """
    {
      "type": "dmss://test-DS/root_package/Parent",
      "name": "parentEntity",
      "description": "",
      "SomeChild": {}
    }
    """

  Given there exist document with id "7" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "Hobby",
      "description": "",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "attributes": [
        {
        "name": "difficulty",
        "attributeType": "string",
        "type": "dmss://system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """

  Given there exist document with id "8" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "Comment",
      "description": "a comment blueprint, that does not require a name",
      "attributes": [
        {
          "name": "type",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        },
        {
          "name": "description",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "default": "",
          "optional": true
        },
        {
          "name": "text",
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute"
        }
      ]
    }
    """

  Scenario: Add file - attribute for parentEntity
    Given i access the resource url "/api/documents/test-DS/$6.SomeChild"
    When i make a form-data "POST" request
    """
    {
      "document": {
        "name": "baseChildInParentEntity",
        "type": "dmss://test-DS/root_package/BaseChild",
        "description": "base child in parent",
        "AValue": 0
      }
    }
    """
    Then the response status should be "OK"
    Given I access the resource url "/api/documents/test-DS/$6"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
          "_id": "6",
          "name": "parentEntity",
          "type": "dmss://test-DS/root_package/Parent",
          "description": "",
          "SomeChild":
          {
            "name": "baseChildInParentEntity",
            "type": "dmss://test-DS/root_package/BaseChild",
            "description": "base child in parent",
            "AValue": 0
          }
    }
    """

  Scenario: Add file (rootPackage) to root of data_source
    Given i access the resource url "/api/documents/test-DS"
    When i make a form-data "POST" request
    """
    {
      "document": {
        "name": "newRootPackage",
        "type": "dmss://system/SIMOS/Package",
        "isRoot": true,
        "content": []
      }
    }
    """
    Then the response status should be "OK"

  Scenario: Add file with wrong subtype to parent entity
    Given i access the resource url "/api/documents/test-DS/$6.SomeChild"
    When i make a form-data "POST" request
    """
    {
      "document": {
        "name": "hobbynumber1",
        "type": "dmss://test-DS/root_package/Hobby",
        "description": "example hobby",
        "difficulty": "high"
      }
    }
    """
    Then the response status should be "Bad Request"
    Given I access the resource url "/api/documents/test-DS/$6"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
          "_id": "6",
          "name": "parentEntity",
          "type": "dmss://test-DS/root_package/Parent",
          "description": "",
          "SomeChild": {}
    }
    """

  Scenario: Add file with an extended type to parent entity
    Given i access the resource url "/api/documents/test-DS/$6.SomeChild"
    When i make a form-data "POST" request
    """
    {
      "document" : {
        "name": "specialChild",
        "type": "dmss://test-DS/root_package/SpecialChild",
        "description": "specialized child",
        "AValue": 39,
        "AnExtraValue": "abc",
        "Hobbies": [
          {
            "name": "Football",
            "type": "dmss://test-DS/root_package/Hobby",
            "description": "sport",
            "difficulty": "high"
          }
        ]
      }
    }
    """
    Then the response status should be "OK"
    Given I access the resource url "/api/documents/test-DS/$6"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
          "_id": "6",
          "name": "parentEntity",
          "type": "dmss://test-DS/root_package/Parent",
          "description": "",
          "SomeChild":
          {
            "name": "specialChild",
            "type": "dmss://test-DS/root_package/SpecialChild",
            "description": "specialized child",
            "AValue": 39,
            "AnExtraValue": "abc"
          }
    }
    """

  Scenario: Add file - not contained
    Given i access the resource url "/api/documents/test-DS/$1.content"
    When i make a form-data "POST" request
    """
    {
      "document" : {
        "name": "new_document",
        "type": "dmss://system/SIMOS/Blueprint"
      }
    }
    """
    Then the response status should be "OK"
    Given I access the resource url "/api/documents/test-DS/$1?depth=99"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
          "name":"root_package",
          "type":"dmss://system/SIMOS/Package",
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
    Given i access the resource url "/api/documents/test-DS/$6.whatever"
    When i make a form-data "POST" request
    """
    {
      "document": {}
    }
    """
    Then the response status should be "Bad Request"
    And the response should contain
    """
    {
    "status": 400,
    "type": "ValidationException",
    "message": "Every entity must have a 'type' attribute",
    "debug": "Location: Entity in key '^'"
    }
    """

  Scenario: Add file to parent that does not exists
    Given i access the resource url "/api/documents/test-DS/$-1.documents"
    When i make a form-data "POST" request
    """
    {
      "document": {
        "name": "new_document",
        "type": "dmss://system/SIMOS/Blueprint"
      }
    }
    """
    Then the response status should be "Not Found"
    And the response should be
    """
    {
    "data": null,
    "debug": "Document with id '-1' was not found in the 'test-DS' data-source. The requested resource could not be found",
    "message": "Failed to get document referenced with 'dmss://test-DS/$-1'",
    "status": 404,
    "type": "NotFoundException"
    }
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
    Given i access the resource url "/api/documents/test-DS/$1.content"
    When i make a form-data "POST" request
    """
    {
      "document": {
        "name": "new_document",
        "type": "dmss://system/SIMOS/Blueprint"
      }
    }
    """
    Then the response status should be "Forbidden"
    And the response should be
    """
    {
    "status": 403,
    "type": "MissingPrivilegeException",
    "message": "The requested operation requires 'WRITE' privileges",
    "debug": "Action denied because of insufficient permissions",
    "data": null
    }
    """

  Scenario: Add file with duplicate name
    Given i access the resource url "/api/documents/test-DS/root_package"
    When i make a "POST" request with "1" files
    """
      {
        "document": {
          "type": "dmss://test-DS/root_package/Parent",
          "name": "parentEntity",
          "description": "",
          "SomeChild": {}
        }
      }
    """
    Then the response status should be "Bad Request"
    And the response should be
    """
    {
    "status": 400,
    "type": "BadRequestException",
    "message": "The document 'test-DS/root_package/parentEntity' already exists",
    "debug": "Unable to complete the requested operation with the given input values.",
    "data": null
    }
    """

  Scenario: Add Comment entity without a name attribute with add-raw endpoint
    Given i access the resource url "/api/documents-add-raw/test-DS"
    When i make a "POST" request
    """
    {
        "_id": "429cb3da-ebbe-4ea6-80a6-b6bca0f67aaa",
        "type": "dmss://test-DS/root_package/Comment",
        "description": "comment entity with no name",
        "text": "example comment"
    }
    """
    Then the response status should be "OK"

  Scenario: Add Parent entity without a name attribute with -by-path endpoint
    Given i access the resource url "/api/documents/test-DS/root_package"
    When i make a "POST" request with "1" files
    """
    {
      "document": {
        "type": "dmss://test-DS/root_package/Parent",
        "description": "parent entity with no name"
      }
    }
    """
    Then the response status should be "Bad Request"
    And the response should contain
    """
    {
      "status": 400,
      "type": "ValidationException",
      "message": "Missing required attribute 'name'",
      "debug": "Location: Entity in key '^'"
    }
    """

  Scenario: Adding file with id set to empty string should generate new uid
    Given I access the resource url "/api/documents/test-DS/root_package"
    When i make a "POST" request with "1" files
    """
    {
      "document": {
        "_id": "",
        "type":"dmss://system/SIMOS/Blueprint",
        "name": "new_bp",
        "description": "Blueprint with no name"
      }
    }
    """
    Then the response status should be "OK"
    And the response should have valid uid

  Scenario: Adding file with id
    Given I access the resource url "/api/documents/test-DS/root_package"
    When i make a "POST" request with "1" files
    """
    {
      "document": {
        "_id": "2283c9b0-d509-46c9-a153-94c79f4d7b7b",
        "type":"dmss://system/SIMOS/Blueprint",
        "name": "new_bp",
        "description": "Blueprint with no name"
      }
    }
    """
    Then the response status should be "OK"
    And the response should have valid uid

  Scenario: Add Comment entity without a name attribute with -by-path endpoint
    Given i access the resource url "/api/documents/test-DS/root_package"
    When i make a "POST" request with "1" files
    """
    {
      "document":
      {
        "type": "dmss://test-DS/root_package/Comment",
        "description": "comment entity with no name",
        "text": "example comment"
      }
    }
    """
    Then the response status should be "OK"

  Scenario: Add blueprint without a name attribute with -by-path endpoint should fail
    Given i access the resource url "/api/documents/test-DS/root_package"
    When i make a "POST" request with "1" files
    """
    {
      "document":
      {
        "type":"dmss://system/SIMOS/Blueprint",
        "description": "Blueprint with no name"
      }
    }
    """
    Then the response status should be "Bad Request"
    And the response should contain
    """
    {
      "status": 400,
      "type": "ValidationException",
      "message": "Missing required attribute 'name'",
      "debug": "Location: Entity in key '^'"
    }
    """

  Scenario: Add package without a name attribute with -by-path endpoint should fail
    Given i access the resource url "/api/documents/test-DS/root_package"
    When i make a "POST" request with "1" files
    """
    {
      "document":
      {
        "type":"dmss://system/SIMOS/Package",
        "description": "Package with no name"
      }
    }
    """
    Then the response status should be "Bad Request"
    And the response should contain
    """
    {
      "status": 400,
      "type": "ValidationException",
      "message": "Missing required attribute 'name'",
      "debug": "Location: Entity in key '^'"
    }
    """

  Scenario: Add parent entity without a name attribute with add_by_parent_id endpoint
    Given i access the resource url "/api/documents/test-DS/1.content"
    When i make a form-data "POST" request
    """
    {
      "document": {
        "type": "dmss://test-DS/root_package/Parent",
        "description": "parent entity with no name"
      }
    }
    """
    Then the response status should be "Bad Request"
    And the response should contain
    """
    {
      "status": 400,
      "type": "ValidationException",
      "message": "Missing required attribute 'name'",
      "debug": "Location: Entity in key '^'"
    }
    """

  Scenario: Add comment entity without a name attribute with add_by_parent_id endpoint
    Given i access the resource url "/api/documents/test-DS/$1.content"
    When i make a form-data "POST" request
    """
    {
      "document": {
        "type": "dmss://test-DS/root_package/Comment",
        "description": "comment entity with no name",
        "text": "example comment"
      }
    }
    """
    Then the response status should be "OK"

  Scenario: Add blueprint without a name using add_by_parent_id endpoint should fail
    Given i access the resource url "/api/documents/test-DS/$1.content"
    When i make a form-data "POST" request
    """
    {
      "document" : {
        "type":"dmss://system/SIMOS/Blueprint",
        "description": "Blueprint with no name"
      }
    }
    """
    Then the response status should be "Bad Request"
    And the response should contain
    """
    {
      "status": 400,
      "type": "ValidationException",
      "message": "Missing required attribute 'name'",
      "debug": "Location: Entity in key '^'"
    }
    """

  Scenario: Add package without a name using add_by_parent_id endpoint should fail
    Given i access the resource url "/api/documents/test-DS/$1.content"
    When i make a form-data "POST" request
    """
    {
      "document": {
        "type":"dmss://system/SIMOS/Package",
        "description": "Package with no name"
      }
    }
    """
    Then the response status should be "Bad Request"
    And the response should contain
    """
    {
      "status": 400,
      "type": "ValidationException",
      "message": "Missing required attribute 'name'",
      "debug": "Location: Entity in key '^'"
    }
    """

  Scenario: Add file with multiple PDFs
    Given i access the resource url "/api/documents/test-DS/root_package"
    When i make a "POST" request with "4" files
    """
    {
      "document": {
        "name": "new_pdf_container",
        "type": "dmss://test-DS/root_package/MultiplePdfContainer",
        "description": "multiple pdf container",
        "a_pdf": {
          "name": "MyPDF1",
          "description": "",
          "type": "dmss://system/SIMOS/PDF",
          "blob": {
            "name": "file1",
            "type": "dmss://system/SIMOS/Blob"
          },
          "author": "Stig Oskar"
        },
        "another_pdf": {
          "name": "MyPDF2",
          "description": "",
          "type": "dmss://system/SIMOS/PDF",
          "blob": {
            "name": "file2",
            "type": "dmss://system/SIMOS/Blob"
          },
          "author": "Stig Oskar"
        },
        "pdf_container": {
          "name": "second_pdf_container",
          "type": "dmss://test-DS/root_package/MultiplePdfContainer",
          "description": "another multiple pdf container",
          "a_pdf": {
            "name": "MyPDF3",
            "description": "",
            "type": "dmss://system/SIMOS/PDF",
            "blob": {
              "name": "file3",
              "type": "dmss://system/SIMOS/Blob"
            },
            "author": "Stig Oskar"
          },
          "another_pdf": {
            "name": "MyPDF4",
            "description": "",
            "type": "dmss://system/SIMOS/PDF",
            "blob": {
              "name": "file4",
              "type": "dmss://system/SIMOS/Blob",
              "size": 0
            },
            "author": "Stig Oskar"
          },
          "pdf_container": {}
        }
      }
    }
    """
    Then the response status should be "OK"