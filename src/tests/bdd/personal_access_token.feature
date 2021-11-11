Feature: Personal Access Token

  Background: The core package is uploaded to the system
    Given the system data source and SIMOS core package are available

  Scenario: Create a PAT
    Given the logged in user is "johndoe" with roles "a"
    Given authentication is enabled
    And I access the resource url "/api/v1/token"
    When I make a "GET" request
    Then the response status should be "OK"
    And the JWT response should contain
    """
    {
    "username": "johndoe",
    "fullname": null,
    "email": null,
    "roles": ["a"],
    "iss": "dmss"
    }
    """
    Then the PAT is valid