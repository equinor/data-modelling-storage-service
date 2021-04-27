Feature: Explorer - Remove by path

  Background: There are data sources in the system

    Given there are data sources
      | name             |
      | data-source-name |
      | blueprints       |
      | system           |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name      | database | collection     | type     | dataTypes |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1     | local    | documents      | mongo-db | default   |
      | SSR-DataSource   | db   | 27017 | maf      | maf      | false | blob-repo | local    | SSR-DataSource | mongo-db | default   |
      | system           | db   | 27017 | maf      | maf      | false | system    | local    | system         | mongo-db | default   |

    Given SIMOS core package are imported

    Given there are documents for the data source "data-source-name" in collection "documents"
      | uid | parent_uid | name          | description | type                   |
      | 1   |            | blueprints    |             | system/SIMOS/Package     |
      | 2   | 1          | sub_package_1 |             | system/SIMOS/Package     |
      | 4   | 1          | sub_package_2 |             | system/SIMOS/Package     |
      | 3   | 2          | document_1    |             | system/SIMOS/Blueprint |

  Scenario: Remove root package
    Given i access the resource url "/api/v1/explorer/data-source-name/remove-by-path"
    When i make a "POST" request
  """
  {
    "directory": "blueprints"
  }
  """
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/data-source-name/1"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should equal
  """
  {"type": "RESOURCE_ERROR", "message": "The entity, with id 1 is not found"}
  """
    Given I access the resource url "/api/v1/documents/data-source-name/2"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should equal
  """
  {"type": "RESOURCE_ERROR", "message": "The entity, with id 2 is not found"}
  """
    Given I access the resource url "/api/v1/documents/data-source-name/3"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should equal
  """
  {"type": "RESOURCE_ERROR", "message": "The entity, with id 3 is not found"}
  """

  Scenario: Remove file with no children
    Given i access the resource url "/api/v1/explorer/data-source-name/remove-by-path"
    When i make a "POST" request
    """
    {
      "directory": "blueprints/sub_package_1"
    }
    """
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/data-source-name/1"
    When I make a "GET" request
    Then the array at document.content should be of length 1

    Given I access the resource url "/api/v1/documents/data-source-name/2"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should equal
    """
    {"type": "RESOURCE_ERROR", "message": "The entity, with id 2 is not found"}
    """

  Scenario: Remove file with no children
    Given i access the resource url "/api/v1/explorer/data-source-name/remove-by-path"
    When i make a "POST" request
    """
    {
      "directory": "blueprints/sub_package_1/document_1"
    }
    """
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/data-source-name/3"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should equal
    """
    {"type": "RESOURCE_ERROR", "message": "The entity, with id 3 is not found"}
    """

  Scenario: Remove file with children
    Given i access the resource url "/api/v1/explorer/data-source-name/remove-by-path"
    When i make a "POST" request
  """
  {
      "directory": "blueprints/sub_package_1"
    }
  """
    Then the response status should be "OK"
    Given I access the resource url "/api/v1/documents/data-source-name/2"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should equal
  """
  {"type": "RESOURCE_ERROR", "message": "The entity, with id 2 is not found"}
  """
    Given I access the resource url "/api/v1/documents/data-source-name/3"
    When I make a "GET" request
    Then the response status should be "Not Found"
    And the response should equal
  """
  {"type": "RESOURCE_ERROR", "message": "The entity, with id 3 is not found"}
  """

