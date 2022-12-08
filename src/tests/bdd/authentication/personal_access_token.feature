Feature: Personal Access Token
  Background: The core package is uploaded to the system and there exist a document in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |

  Scenario: Create a PAT
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    And I access the resource url "/api/v1/token"
    When I make a "POST" request
    Then the response status should be "OK"
    And the PAT is added to context
    And I access the resource url "/api/v1/whoami"
    When I make a "GET" request
    Then the response status should be "OK"

 Scenario: Create a PAT with READ, try to write with it
    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "Whatever",
      "attributes": [
        {
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "Something"
        }
      ]
    }
    """
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "someoneelse",
      "users": { "johndoe": "READ"}
    }
    """
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    And I access the resource url "/api/v1/token?scope=READ"
    When I make a "POST" request
    Then the response status should be "OK"
    And the PAT is added to context
    Given i access the resource url "/api/v1/documents/test-DS/1"
    When i make a "DELETE" request
    Then the response status should be "Forbidden"


  Scenario: Create a PAT using another PAT
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    And I access the resource url "/api/v1/token"
    When I make a "POST" request
    Then the response status should be "OK"
    And the PAT is added to context
    And the PAT is added to headers
    And I access the resource url "/api/v1/token"
    When I make a "POST" request
    Then the response status should be "Unauthorized"

  Scenario: Catch an expired PAT
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    And I access the resource url "/api/v1/token?time_to_live=1"
    When I make a "POST" request
    Then the response status should be "OK"
    And the PAT is added to context
    And the PAT is added to headers
    Then the PAT is expired

  Scenario: Use PAT with lacking privileges
    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "Whatever",
      "attributes": [
        {
          "attributeType": "string",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "name": "Something"
        }
      ]
    }
    """
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "johndoe",
      "others": "NONE"
    }
    """
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    And I access the resource url "/api/v1/token?scope=READ"
    When I make a "POST" request
    Then the response status should be "OK"
    And the PAT is added to context
    And the PAT is added to headers
    Given i access the resource url "/api/v1/documents/test-DS/1"
    When i make a "DELETE" request
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

  Scenario: List all users PAT's
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    And I access the resource url "/api/v1/token"
    When I make a "POST" request
    Then the response status should be "OK"
    And I access the resource url "/api/v1/token"
    When I make a "GET" request
    Then the response status should be "OK"

  Scenario: Revoke a PAT
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    And I access the resource url "/api/v1/token"
    When I make a "POST" request
    Then the response status should be "OK"
    And the PAT is added to context
    When I access the resource url "/api/v1/token"
    And I make a "GET" request
    Then the response status should be "OK"
    And the PAT is revoked
    And the PAT is added to headers
    When I access the resource url "/api/v1/whoami"
    And I make a "GET" request
    Then the response status should be "Unauthorized"
