Feature: Validate entities in database

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available


  Scenario: Validate existing SIMOS CORE
    Given i access the resource url "/api/entity/validate-existing-entity/system/SIMOS/"
    When i make a "POST" request
    Then the response status should be "OK"


