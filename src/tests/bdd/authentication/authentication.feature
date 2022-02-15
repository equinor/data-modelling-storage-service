Feature: Authentication

  Background: The core package is uploaded to the system
    Given the system data source and SIMOS core package are available

  Scenario: Get current user
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    And I access the resource url "/api/v1/whoami"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should equal
    """
    {
    "username_id": "johndoe",
    "full_name": null,
    "email": null,
    "roles": ["a"],
    "scope": 2
    }
    """

