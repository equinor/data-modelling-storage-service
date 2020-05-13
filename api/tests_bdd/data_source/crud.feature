Feature: Data Sources

  Background: There are data sources in the system

    Given there are mongodb data sources
      | host | port  | username | password | tls   | name           | database | collection     | type     |
      | db   | 27017 | maf      | maf      | false | entities       | local    | documents      | mongo-db |
      | db   | 27017 | maf      | maf      | false | SSR-DataSource | local    | SSR-DataSource | mongo-db |
      | db   | 27017 | maf      | maf      | false | system         | local    | system         | mongo-db |

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
      {
        "name": "Local workspace"
      },
      {
        "name": "entities"
      },
      {
        "name": "SSR-DataSource"
      }
    ]
    """

  Scenario: Create new data source
    Given i access the resource url "/api/v1/data-sources/myTest-DataSource"
    And data modelling tool templates are imported
    When i make a "POST" request
    """
    {
      "name": "myTest-DataSource",
      "repositories": {
        "myTest-DataSource": {
          "type": "mongo-db",
          "host": "database-server.equinor.com",
          "port": 27017,
          "username": "test",
          "password": "testpassword",
          "tls": false,
          "name": "myTest-DataSource",
          "database": "mariner",
          "collection": "blueprints"
        }
      }
    }
    """
    Then the response status should be "OK"
