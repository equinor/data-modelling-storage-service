Feature: Explorer - Add file

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |
    Given there are documents for the data source "test-DS" in collection "documents"
      | uid | parent_uid | name         | description | type                   |
      | 1   |            | root_package |             | system/SIMOS/Package     |
      | 2   | 1          | document_1   |             | system/SIMOS/Blueprint |
      | 3   | 1          | document_2   |             | system/SIMOS/Blueprint |

  @skip
  Scenario: Rename package
    Given i access the resource url "/api/v1/explorer/test-DS/rename"
    When i make a "PUT" request
    """
    {
      "parentId": null,
      "documentId": "1",
      "name": "new_root_package_name"
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "uid": "1"
    }
    """
  @skip
  Scenario: Rename blueprint
    Given i access the resource url "/api/v1/explorer/test-DS/rename"
    When i make a "PUT" request
    """
    {
      "parentId": "1",
      "documentId": "2",
      "name": "new_blueprint_name"
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {
      "uid": "2"
    }
    """

  @skip
  Scenario: Try to rename a document that does not exists
    Given i access the resource url "/api/v1/explorer/test-DS/rename"
    When i make a "PUT" request
    """
    {
      "parentId": "1",
      "documentId": "10",
      "name": "new_blueprint_name"
    }
    """
    Then the response status should be "Not Found"
    And the response should be
    """
    EntityNotFoundException: The entity, with id 10 could not be found
    """

  @skip
  Scenario: Try to rename a document with a parent that does not exists
    Given i access the resource url "/api/v1/explorer/test-DS/rename"
    When i make a "PUT" request
    """
    {
      "parentId": "10",
      "documentId": "2",
      "name": "new_blueprint_name"
    }
    """
    Then the response status should be "Not Found"
    And the response should be
    """
    EntityNotFoundException: Document with id '10' was not found in the 'test-DS' data-source
    """

  @skip
  Scenario: Try to rename a document to equal name as another document
    Given i access the resource url "/api/v1/explorer/test-DS/rename"
    When i make a "PUT" request
    """
    {
      "parentId": "1",
      "documentId": "3",
      "name": "document_1"
    }
    """
    Then the response should be "Unprocessable Entity"
    And the response should equal
    """
    {
      "type": "SYSTEM_ERROR",
      "message": "EntityAlreadyExistsException: 'The document, with id document_1 already exists'"
    }
    """
