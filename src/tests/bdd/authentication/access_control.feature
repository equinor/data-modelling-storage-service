Feature: Access Control

  Background: There exist a document in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |

    Given there are repositories in the data sources
      | data-source | host | port  | username | password | tls   | name  | database  | collection | type     | dataTypes |
      |  test-DS    | db   | 27017 | maf      | maf      | false | blobs |  bdd-test | blobs      | mongo-db | blob      |

    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "Whatever",
      "attributes": [
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "Something"
        }
      ]
    }
    """

  Scenario: Get owned document
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "johndoe"
    }
    """
    Given the logged in user is "johndoe" with roles "a,b"
    Given authentication is enabled
    Given I access the resource url "/api/v1/documents/test-DS/1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "Whatever",
      "attributes": [
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "Something"
        }
      ]
    }
    """

  Scenario: Get document with no access
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "somebody",
      "others": "NONE"
    }
    """
    Given the logged in user is "johndoe" with roles "a,b"
    Given authentication is enabled
    Given I access the resource url "/api/v1/documents/test-DS/1"
    When I make a "GET" request
    Then the response status should be "Forbidden"
    And the response should be
    """
    MissingPrivilegeException: The requested operation requires 'READ' privileges
    """

  Scenario: Get document with read access from role
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "somebody",
      "others": "NONE",
      "roles": {
        "anotherRole": "NONE",
        "someRole": "READ"
      }
    }
    """
    Given the logged in user is "johndoe" with roles "someRole,anotherRole"
    Given authentication is enabled
    Given I access the resource url "/api/v1/documents/test-DS/1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "Whatever",
      "attributes": [
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "Something"
        }
      ]
    }
    """

  Scenario: Get document with read access from users
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "somebody",
      "others": "NONE",
      "roles": {
        "anotherRole": "NONE",
        "someRole": "NONE"
      },
      "users": {
        "johndoe": "WRITE"
      }
    }
    """
    Given the logged in user is "johndoe" with roles "someRole,anotherRole"
    Given authentication is enabled
    Given I access the resource url "/api/v1/documents/test-DS/1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "Whatever",
      "attributes": [
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "Something"
        }
      ]
    }
    """

  Scenario: Update owned document
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "johndoe"
    }
    """
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    Given I access the resource url "/api/v1/documents/test-DS/1"
    When i make a form-data "PUT" request
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "Whatever",
      "attributes": [
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "ChangedName"
        }
      ]
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "data": {
        "type": "system/SIMOS/Blueprint",
        "name": "Whatever",
        "attributes": [
          {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "ChangedName"
          }
        ]
      }
    }
    """

  Scenario: Update document with only READ access
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "someoneElse",
      "others": "NONE",
      "users": {
        "johndoe": "READ"
      }
    }
    """
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    Given I access the resource url "/api/v1/documents/test-DS/1"
    When i make a form-data "PUT" request
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "Whatever",
      "attributes": [
        {
          "attributeType": "string",
          "type": "system/SIMOS/BlueprintAttribute",
          "name": "ChangedName"
        }
      ]
    }
    """
    Then the response status should be "Forbidden"
    And the response should be
    """
    MissingPrivilegeException: The requested operation requires 'WRITE' privileges
    """

  Scenario: Delete document with only READ access
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "someoneElse"
    }
    """
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    Given i access the resource url "/api/v1/explorer/test-DS/1"
    When i make a "DELETE" request
    Then the response status should be "Forbidden"
    And the response should contain
    """
    {
    "type": "FORBIDDEN",
    "message": "MissingPrivilegeException: The requested operation requires 'WRITE' privileges"
    }
    """

  Scenario: Delete owned document
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "johndoe"
    }
    """
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    Given i access the resource url "/api/v1/explorer/test-DS/1"
    When i make a "DELETE" request
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/test-DS/1"
    When I make a "GET" request
    Then the response status should be "Not Found"

  Scenario: Get blob with no access
    Given there exists a blob with id "1234" in data source "test-DS" loaded from "tests/bdd/steps/test_pdf.pdf"
    Given AccessControlList for document "1234" in data-source "test-DS" is
    """
    {
      "owner": "someoneElse",
      "others": "NONE"
    }
    """
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    Given i access the resource url "/api/v1/blobs/test-DS/1234"
    When i make a "GET" request
    Then the response status should be "Forbidden"
    And the response should contain
    """
    {
    "type": "FORBIDDEN",
    "message": "MissingPrivilegeException: The requested operation requires 'READ' privileges"
    }
    """

  Scenario: Add file - not contained - inherit ACL
    Given there exist document with id "2" in data source "test-DS"
    """
    {
        "name": "root_package",
        "description": "",
        "type": "system/SIMOS/Package",
        "isRoot": true,
        "content": []
    }
    """
    Given AccessControlList for document "2" in data-source "test-DS" is
    """
    {
      "owner": "johndoe",
      "roles": {"someRole": "WRITE", "someOtherRole": "READ"},
      "users": {"per": "WRITE", "pål": "READ"},
      "others": "NONE"
    }
    """
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    Given i access the resource url "/api/v1/explorer/test-DS/2.content"
    When i make a "POST" request
    """
    {
      "_id": "3",
      "name": "new_document",
      "type": "system/SIMOS/Blueprint"
    }
    """
    Then the response status should be "OK"
