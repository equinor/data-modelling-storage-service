Feature: Explorer - Add Root Package

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      | name    |
      | test-DS |

  Scenario: Add root package
    Given i access the resource url "/api/v1/explorer/test-DS/add-package"
    When i make a "POST" request
    """
    {
      "name": "new_root_package",
      "type": "system/SIMOS/Package"
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {
        "data":{
           "name":"new_root_package",
           "type":"system/SIMOS/Package",
           "isRoot":true
        }
    }
    """
  Scenario: Add root package lacking permissions
    Given AccessControlList for data-source "test-DS" is
    """
    {
      "owner": "dmss-admin",
      "others": "READ"
    }
    """
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    Given i access the resource url "/api/v1/explorer/test-DS/add-package"
    When i make a "POST" request
    """
    {
      "name": "new_root_package",
      "type": "system/SIMOS/Package"
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

  Scenario: Add root package with missing parameter name should fail
    Given i access the resource url "/api/v1/explorer/test-DS/add-package"
    When i make a "POST" request
    """
    {
      "type": "system/SIMOS/Package"
    }
    """
    Then the response status should be "Unprocessable Entity"
    And the response should equal
    """
    {"detail": [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]}
    """
