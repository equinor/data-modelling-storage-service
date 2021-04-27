Feature: Data Sources

  Background: There are data sources in the system

    Given there are data sources
      |       name         |
      | entities   |
      | SSR-DataSource   |
      | system             |

    Given there are repositories in the data sources
      | data-source    | host | port  | username | password | tls   | name      | database | collection     | type     | dataTypes |
      | entities       | db   | 27017 | maf      | maf      | false | repo1     | local    | documents      | mongo-db | default   |
      | SSR-DataSource | db   | 27017 | maf      | maf      | false | blob-repo | local    | SSR-DataSource | mongo-db | default   |
      | system         | db   | 27017 | maf      | maf      | false | system    | local    | system         | mongo-db | default   |

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
      },
      {
        "name": "system"
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

  Scenario: Update existing data source
    Given i access the resource url "/api/v1/data-sources/myTest-DataSource"
    And data modelling tool templates are imported
    When i make a "POST" request
    """
    {
      "name": "myTest-DataSource",
      "repositories": {
        "myTest-DataSource": {
          "type": "mongo-db",
          "host": "new-database-server.equinor.com/",
          "port": 27017,
          "username": "new_username",
          "password": "new_password",
          "tls": false,
          "name": "myTest-DataSource",
          "database": "mariner",
          "collection": "blueprints"
        }
      }
    }
    """
    Then the response status should be "OK"
    

  Scenario: Create new data source with multiple repositories
    Given i access the resource url "/api/v1/data-sources/MyMultiRepDS"
    And data modelling tool templates are imported
    When i make a "POST" request
    """
    {
      "name": "MyMultiRepDS",
      "repositories": {
        "myMongoRepo": {
          "type": "mongo-db",
          "host": "database-server.equinor.com",
          "port": 27017,
          "username": "test",
          "password": "testpassword",
          "tls": false,
          "name": "myMongoRepo",
          "database": "mariner",
          "collection": "blueprints"
        },
        "myAzureRepo": {
          "type": "azure-blob-storage",
          "account_name": "dmssfilestorage",
          "account_key": "a-long-key",
          "name": "myAzureRepo",
          "collection": "dmss",
          "documentType": "blueprints"
        }
      }
    }
    """
    Then the response status should be "OK"
