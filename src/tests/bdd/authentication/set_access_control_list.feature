Feature: Set Access Control List

  Background: There exist a document in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |

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

  Scenario: Grant additional role write
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "johndoe"
    }
    """
    Given the logged in user is "johndoe" with roles "a,b"
    Given authentication is enabled
    Given I access the resource url "/api/v1/acl/test-DS/1"
    When I make a "PUT" request
    """
    {
      "owner": "johndoe",
      "roles": {
        "test": "WRITE"
      }
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    "OK"
    """
    Then I access the resource url "/api/v1/acl/test-DS/1"
    Given the logged in user is "johndoe" with roles "a,b"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "owner": "johndoe",
      "roles": {
        "test": "WRITE"
      }
    }
    """

  Scenario: Grant additional role write with lacking permission
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "someoneElse"
    }
    """
    Given the logged in user is "johndoe" with roles "a,b"
    Given authentication is enabled
    Given I access the resource url "/api/v1/acl/test-DS/1"
    When I make a "PUT" request
    """
    {
      "owner": "johndoe",
      "roles": {
        "test": "WRITE"
      }
    }
    """
    Then the response status should be "Forbidden"
    And the response should contain
    """
    {
    "type": "FORBIDDEN",
    "message": "MissingPrivilegeException: The requested operation requires 'WRITE' privileges"
    }
    """
    Then I access the resource url "/api/v1/acl/test-DS/1"
    Given the logged in user is "johndoe" with roles "a,b"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "owner": "someoneElse"
    }
    """

  Scenario: Fetch ACL with lacking permission
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "someoneElse",
      "others": "NONE"
    }
    """
    Given the logged in user is "johndoe" with roles "a,b"
    Given authentication is enabled
    Given I access the resource url "/api/v1/acl/test-DS/1"
    Given the logged in user is "johndoe" with roles "a,b"
    When I make a "GET" request
    Then the response status should be "Forbidden"
    And the response should contain
    """
    {
    "type": "FORBIDDEN",
    "message": "MissingPrivilegeException: The requested operation requires 'READ' privileges"
    }
    """
