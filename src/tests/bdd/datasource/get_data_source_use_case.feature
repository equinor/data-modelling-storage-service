Feature: Get data source use case

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      |    name  |
      | entities |
      | demo-DS  |

    Given there are repositories in the data sources
      | data-source | host | port  | username | password | tls   | name      | database | collection     | type     | dataTypes |
      | entities    | db   | 27017 | maf      | maf      | false | repo1     |  bdd-test    | documents      | mongo-db | default   |
      | demo-DS     | db   | 27017 | maf      | maf      | false | blob-repo |  bdd-test    | demo-DS        | mongo-db | default   |


  Scenario: Get single data source
    Given I access the resource url "/api/v1/data-sources/system"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "name": "system",
      "id": "system"
    }
    """

  Scenario: Get all data sources
    Given I access the resource url "/api/v1/data-sources"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    [
      {},
      {
        "name": "entities"
      },
      {
        "name": "demo-DS"
      }
    ]
    """