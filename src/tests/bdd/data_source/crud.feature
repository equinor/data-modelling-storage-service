Feature: Data Sources

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
    Given I access the resource url "/api/data-sources/system"
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
    Given I access the resource url "/api/data-sources"
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

  Scenario: Create new data source
    Given i access the resource url "/api/data-sources/myTest-DataSource"
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

  Scenario: Create new data source with multiple repositories
    Given i access the resource url "/api/data-sources/MyMultiRepDS"
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
          "account_url": "an-azure-blob-storage-url-with-sas-token",
          "name": "myAzureRepo",
          "collection": "dmss",
          "documentType": "blueprints"
        }
      }
    }
    """
    Then the response status should be "OK"

  Scenario: Try to create a new data source but with an invalid request body
    Given i access the resource url "/api/data-sources/myTest-DataSource"
    When i make a form-data "POST" request
    """
    { "data": "this is not valid json"}
    """
    Then the response status should be "Unprocessable Entity"
    And the response should contain
    """
    {
    "status": 422,
    "type": "RequestValidationError",
    "message": "The received values are invalid",
    "debug": "The received values are invalid according to the endpoints model definition",
    "data": {
      "body": "data=this+is+not+valid+json",
      "detail": [
          {
            "loc": [
              "body"
            ],
            "msg": "value is not a valid dict",
            "type": "type_error.dict"
          }
        ]
      }
    }
    """