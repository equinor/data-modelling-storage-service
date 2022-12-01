Feature: Create a lookup table
    Background: There are data sources in the system
    Given the system data source and SIMOS core package are available

  Scenario: System admins want to create a recipe lookup for the DMSS - SIMOS/recipe_links folder
    Given i access the resource url "/api/v1/lookup/system/SIMOS/recipe_links?application=dmss"
    When i make a "POST" request
    Then the response status should be "No Content"
