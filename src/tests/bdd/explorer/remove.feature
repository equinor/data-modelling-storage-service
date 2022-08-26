Feature: Explorer - Remove

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are data sources
      | name             |
      | data-source-name |
      | blueprints       |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name      | database | collection     | type     | dataTypes |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1     |  bdd-test    | documents      | mongo-db | default   |
      | demo-DS   | db   | 27017 | maf      | maf      | false | blob-repo |  bdd-test    | demo-DS | mongo-db | default   |

    Given there are documents for the data source "data-source-name" in collection "documents"
      | uid | parent_uid | name          | description | type                   |
      | 1   |            | blueprints    |             | system/SIMOS/Package     |
      | 2   | 1          | sub_package_1 |             | system/SIMOS/Package     |
      | 4   | 1          | sub_package_2 |             | system/SIMOS/Package     |
      | 3   | 2          | document_1    |             | system/SIMOS/Blueprint |

  Scenario: Remove root package
    Given i access the resource url "/api/v1/explorer/data-source-name/1"
    When i make a "DELETE" request
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/data-source-name/1"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should be
  """
  {
  "status": 404,
  "type": "NotFoundException",
  "message": "Document with id '1' was not found in the 'data-source-name' data-source",
  "debug": "The requested resource could not be found",
  "data": null
  }
  """
    Given I access the resource url "/api/v1/documents/data-source-name/2"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should be
  """
  {
  "status": 404,
  "type": "NotFoundException",
  "message": "Document with id '2' was not found in the 'data-source-name' data-source",
  "debug": "The requested resource could not be found",
  "data": null
  }
  """
    Given I access the resource url "/api/v1/documents/data-source-name/3"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should be
  """
  {
  "status": 404,
  "type": "NotFoundException",
  "message": "Document with id '3' was not found in the 'data-source-name' data-source",
  "debug": "The requested resource could not be found",
  "data": null
  }
  """

  Scenario: Remove file with no children
    Given i access the resource url "/api/v1/explorer/data-source-name/1.content.0"
    When i make a "DELETE" request
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/data-source-name/1"
    When I make a "GET" request
    Then the array at content should be of length 1

    Given I access the resource url "/api/v1/documents/data-source-name/2"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should be
    """
    {
    "status": 404,
    "type": "NotFoundException",
    "message": "Document with id '2' was not found in the 'data-source-name' data-source",
    "debug": "The requested resource could not be found",
    "data": null
    }
    """

  Scenario: Remove another file with no children
    Given i access the resource url "/api/v1/explorer/data-source-name/2.content.0"
    When i make a "DELETE" request
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/data-source-name/3"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should be
    """
    {
    "status": 404,
    "type": "NotFoundException",
    "message": "Document with id '3' was not found in the 'data-source-name' data-source",
    "debug": "The requested resource could not be found",
    "data": null
    }
    """

  Scenario: Remove file with children
    Given i access the resource url "/api/v1/explorer/data-source-name/1.content.0"
    When i make a "DELETE" request
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/data-source-name/2"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should be
  """
  {
  "status": 404,
  "type": "NotFoundException",
  "message": "Document with id '2' was not found in the 'data-source-name' data-source",
  "debug": "The requested resource could not be found",
  "data": null
  }
  """
    Given I access the resource url "/api/v1/documents/data-source-name/3"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should be
  """
  {
  "status": 404,
  "type": "NotFoundException",
  "message": "Document with id '3' was not found in the 'data-source-name' data-source",
  "debug": "The requested resource could not be found",
  "data": null
  }
  """

