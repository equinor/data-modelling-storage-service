Feature: Explorer - Remove by path

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | data-source-name |

    Given there are documents for the data source "data-source-name" in collection "data-source-name"
      | uid | parent_uid | name          | description | type                   |
      | 1   |            | blueprints    |             | dmss://system/SIMOS/Package   |
      | 2   | 1          | sub_package_1 |             | dmss://system/SIMOS/Package   |
      | 4   | 1          | sub_package_2 |             | dmss://system/SIMOS/Package   |
      | 3   | 2          | document_1    |             | dmss://system/SIMOS/Blueprint |

  Scenario: Remove root package by name
    Given i access the resource url "/api/documents/data-source-name/blueprints"
    When i make a "DELETE" request
    Then the response status should be "OK"
    Given I access the resource url "/api/documents/data-source-name/$1"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should be
  """
  {
  "data": {"status": 404, "type": "NotFoundException", "message": "Document with id '1' was not found in the 'data-source-name' data-source", "debug": "The requested resource could not be found", "data": null},
  "debug": "Document with id '1' was not found in the 'data-source-name' data-source",
  "message": "Failed to get document referenced with 'dmss://data-source-name/$1'",
  "status": 404,
  "type": "NotFoundException"
  }
  """
    Given I access the resource url "/api/documents/data-source-name/$2"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should contain
  """
  {
  "debug": "Document with id '2' was not found in the 'data-source-name' data-source",
  "message": "Failed to get document referenced with 'dmss://data-source-name/$2'",
  "status": 404,
  "type": "NotFoundException"
  }
  """
    Given I access the resource url "/api/documents/data-source-name/$3"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should contain
  """
  {
  "debug": "Document with id '3' was not found in the 'data-source-name' data-source",
  "message": "Failed to get document referenced with 'dmss://data-source-name/$3'",
  "status": 404,
  "type": "NotFoundException"
  }
  """

  Scenario: Remove subpackage with child
    Given i access the resource url "/api/documents/data-source-name/blueprints/sub_package_1"
    When i make a "DELETE" request
    Then the response status should be "OK"
    Given I access the resource url "/api/documents/data-source-name/$1"
    When I make a "GET" request
    Then the response status should be "OK"
    And the array at content should be of length 1

    Given I access the resource url "/api/documents/data-source-name/$2"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should contain
    """
    {
    "debug": "Document with id '2' was not found in the 'data-source-name' data-source",
    "message": "Failed to get document referenced with 'dmss://data-source-name/$2'",
    "status": 404,
    "type": "NotFoundException"
    }
    """

  Scenario: Remove file with no children
    Given i access the resource url "/api/documents/data-source-name/blueprints"
    When i make a "DELETE" request
    Then the response status should be "OK"
    Given I access the resource url "/api/documents/data-source-name/$3"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should contain
    """
    {
    "debug": "Document with id '3' was not found in the 'data-source-name' data-source",
    "message": "Failed to get document referenced with 'dmss://data-source-name/$3'",
    "status": 404,
    "type": "NotFoundException"
    }
    """

  Scenario: Remove item from list
    Given i access the resource url "/api/documents/data-source-name/blueprints.content[1]"
    When i make a "DELETE" request
    Then the response status should be "OK"
    Given I access the resource url "/api/documents/data-source-name/$4"
    When I make a "GET" request
    Then the response status should be "Not Found"

  Scenario: Remove file with children
    Given i access the resource url "/api/documents/data-source-name/blueprints/sub_package_1"
    When i make a "DELETE" request
    Then the response status should be "OK"
    Given I access the resource url "/api/documents/data-source-name/$2"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should contain
  """
  {
    "debug": "Document with id '2' was not found in the 'data-source-name' data-source",
    "message": "Failed to get document referenced with 'dmss://data-source-name/$2'",
    "status": 404,
    "type": "NotFoundException"
  }
  """
    Given I access the resource url "/api/documents/data-source-name/$3"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should contain
  """
  {
  "debug": "Document with id '3' was not found in the 'data-source-name' data-source",
  "message": "Failed to get document referenced with 'dmss://data-source-name/$3'",
  "status": 404,
  "type": "NotFoundException"
  }
  """

