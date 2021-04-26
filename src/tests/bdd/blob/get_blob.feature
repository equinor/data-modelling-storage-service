Feature: Blob - Get

  Background: There are data sources in the system


    Given there are data sources
      | name   |
      | system |
      | stuff  |
    Given there are repositories in the data sources
      | data-source | host | port  | username | password | tls   | name      | database | collection | type     | dataTypes |
      | system      | db   | 27017 | maf      | maf      | false | system    | local    | system     | mongo-db | default   |
      |  stuff      | db   | 27017 | maf      | maf      | false | blobs     | local    | blobs      | mongo-db | blob      |
      |  stuff      | db   | 27017 | maf      | maf      | false | documents | local    | documents  | mongo-db | default   |
    Given data modelling tool templates are imported
    Given there exists a blob with id "1234" in data source "stuff" loaded from "tests/bdd/steps/test_pdf.pdf"

  Scenario: Get a blob by id
    Given i access the resource url "/api/v1/blobs/stuff/1234"
    When i make a "GET" request
    Then the response status should be "OK"
    And the length of the response should not be zero
