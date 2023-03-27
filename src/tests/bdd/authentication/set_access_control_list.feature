Feature: Set Access Control List

  Background: There exist a document in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |

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
  Given there exist document with id "2" in data source "test-DS"
    """
    {
        "name": "root_package",
        "type": "dmss://system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
                "type": "dmss://system/SIMOS/Link",
                "ref": "3",
                "targetName": "SubPack",
                "targetType": "dmss://system/SIMOS/Package"
            }
        ]
    }
    """
    Given there exist document with id "3" in data source "test-DS"
    """
    {
        "name": "SubPack",
        "type": "dmss://system/SIMOS/Package",
        "content": [
            {
                "type": "dmss://system/SIMOS/Link",
                "ref": "4",
                "targetName": "SubSubPack",
                "targetType": "dmss://system/SIMOS/Package"
            }
        ],
        "isRoot": false
    }
    """
    Given there exist document with id "4" in data source "test-DS"
    """
    {
        "name": "SubSubPack",
        "type": "dmss://system/SIMOS/Package",
        "content": [
        ],
        "isRoot": false
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
    Given I access the resource url "/api/acl/test-DS/1"
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
    And the response should be
    """
    OK
    """
    Then I access the resource url "/api/acl/test-DS/1"
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

  Scenario: Grant additional role write recursively
    Given AccessControlList for document "2" in data-source "test-DS" is
    """
    {
      "owner": "johndoe"
    }
    """
    Given AccessControlList for document "3" in data-source "test-DS" is
    """
    {
      "owner": "johndoe"
    }
    """
    Given AccessControlList for document "4" in data-source "test-DS" is
    """
    {
      "owner": "johndoe"
    }
    """
    Given the logged in user is "johndoe" with roles "a,b"
    Given authentication is enabled
    Given I access the resource url "/api/acl/test-DS/2"
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
    And the response should be
    """
    OK
    """
    Then I access the resource url "/api/acl/test-DS/2"
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
    Then I access the resource url "/api/acl/test-DS/3"
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
    Then I access the resource url "/api/acl/test-DS/4"
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
    Given I access the resource url "/api/acl/test-DS/1"
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
    Then I access the resource url "/api/acl/test-DS/1"
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
    Given I access the resource url "/api/acl/test-DS/1?recursively=false"
    When I make a "GET" request
    Then the response status should be "Forbidden"
    And the response should be
    """
    {
    "status": 403,
    "type": "MissingPrivilegeException",
    "message": "The requested operation requires 'READ' privileges",
    "debug": "Action denied because of insufficient permissions",
    "data": null
    }
    """
