Feature: Files

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      | name    |
      | test-DS |

    Given there are repositories in the data sources
      | data-source | host | port  | username | password | tls   | name      | database | collection | type     | dataTypes |
      | test-DS     | db   | 27017 | maf      | maf      | false | repo1     | bdd-test | documents  | mongo-db | default   |
      | test-DS     | db   | 27017 | maf      | maf      | false | blob-repo | bdd-test | test       | mongo-db | blob      |


  Scenario: Add file
    Given i access the resource url "/api/files/test-DS"
    And adding a binary file "tests/bdd/steps/test_pdf.pdf" to the request
    When i make a "POST" request
    """
    {
      "data": {
        "file_id": "1234"
      }
    }
    """
    Then the response status should be "OK"
    And the response should contain
     """
     {
       "_id": "1234",
       "type": "dmss://system/SIMOS/File",
       "name": "test_pdf",
       "size": 531540,
       "filetype": "pdf",
       "contentType": "application/pdf",
       "content": {
           "type": "dmss://system/SIMOS/Reference",
           "referenceType": "storage"
        }
     }
     """