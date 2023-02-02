Feature: Create a lookup table
    Background: There are data sources in the system
    Given the system data source and SIMOS core package are available

  Scenario: System admins want to create a recipe lookup for the DMSS - SIMOS/recipe_links folder
    Given i access the resource url "/api/application/dmss?recipe_package=system/SIMOS/recipe_links"
    When i make a "POST" request
    Then the response status should be "No Content"

  Scenario: System admins want to replace an existing recipe lookup for DMSS - SIMOS/recipe_links folder
    Given i access the resource url "/api/application/dmss?recipe_package=system/SIMOS/recipe_links"
    When i make a "POST" request
    Then the response status should be "No Content"
    Given i access the resource url "/api/application/dmss?recipe_package=system/SIMOS/recipe_links"
    When i make a "POST" request
    Then the response status should be "No Content"