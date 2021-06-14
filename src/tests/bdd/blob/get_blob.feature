Feature: Blob - Get

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available

    Given there are data sources
      | name   |
      | stuff  |
    Given there are repositories in the data sources
      | data-source | host | port  | username | password | tls   | name      | database | collection | type     | dataTypes |
      |  stuff      | db   | 27017 | maf      | maf      | false | blobs     |  bdd-test    | blobs      | mongo-db | blob      |
      |  stuff      | db   | 27017 | maf      | maf      | false | documents |  bdd-test    | documents  | mongo-db | default   |

    Given there exists a blob with id "1234" in data source "stuff" loaded from "tests/bdd/steps/test_pdf.pdf"

  Scenario: Get a blob by id
    Given i access the resource url "/api/v1/blobs/stuff/1234"
    When i make a "GET" request
    Then the response status should be "OK"
    And the length of the response should not be zero
