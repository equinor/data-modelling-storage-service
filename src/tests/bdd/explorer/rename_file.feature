Feature: Explorer - Add file

  Background: There are data sources in the system

    Given there are data sources
      | name             |
      | data-source-name |
      | blueprints       |
      | system           |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name      | database | collection     | type     | dataTypes |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1     | local    | documents      | mongo-db | default   |
      | demo-DS   | db   | 27017 | maf      | maf      | false | blob-repo | local    | demo-DS | mongo-db | default   |
      | system           | db   | 27017 | maf      | maf      | false | system    | local    | system         | mongo-db | default   |

    Given SIMOS core package are imported

    Given there are documents for the data source "data-source-name" in collection "documents"
      | uid | parent_uid | name         | description | type                   |
      | 1   |            | root_package |             | system/SIMOS/Package     |
      | 2   | 1          | document_1   |             | system/SIMOS/Blueprint |
      | 3   | 1          | document_2   |             | system/SIMOS/Blueprint |

  Scenario: Rename package
    Given i access the resource url "/api/v1/explorer/data-source-name/rename"
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

  Scenario: Rename blueprint
    Given i access the resource url "/api/v1/explorer/data-source-name/rename"
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

  Scenario: Try to rename a document that does not exists
    Given i access the resource url "/api/v1/explorer/data-source-name/rename"
    When i make a "PUT" request
    """
    {
      "parentId": "1",
      "documentId": "10",
      "name": "new_blueprint_name"
    }
    """
    Then the response status should be "Not Found"
    And the response should equal
    """
    {"type": "RESOURCE_ERROR", "message": "The entity, with id 10 is not found"}
    """

  Scenario: Try to rename a document with a parent that does not exists
    Given i access the resource url "/api/v1/explorer/data-source-name/rename"
    When i make a "PUT" request
    """
    {
      "parentId": "10",
      "documentId": "2",
      "name": "new_blueprint_name"
    }
    """
    Then the response status should be "Not Found"
    And the response should equal
    """
    {"type": "RESOURCE_ERROR", "message": "The entity, with id 10 is not found"}
    """

    @skip
  Scenario: Try to rename a document to equal name as another document
    Given i access the resource url "/api/v1/explorer/data-source-name/rename"
    When i make a "PUT" request
    """
    {
      "parentId": "1",
      "documentId": "3",
      "name": "document_1"
    }
    """
    Then the response status should be "System Error"
    And the response should equal
    """
    {
      "type": "SYSTEM_ERROR",
      "message": "EntityAlreadyExistsException: 'The document, with id document_1 already exists'"
    }
    """
