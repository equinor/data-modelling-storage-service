Feature: OAuth2 Authentication

  Background: The core package is uploaded to the system
    Given the system data source and SIMOS core package are available

  Scenario: Get current user without providing token
    Given I access the resource url "/api/v1/whoami"
    When I make a "GET" request
    Then the response status should be "Unauthorized"
    And the response should contain
    """
    {
    "detail": "Not authenticated"
    }
    """

  Scenario: Get current user
    Given I access the resource url "/api/v1/whoami"
    Given the logged in user is "johndoe"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should equal
    """
    {
    "username": "johndoe",
    "full_name": "John Doe",
    "email": "johndoe@example.com",
    "password": "secret"
    }
    """

