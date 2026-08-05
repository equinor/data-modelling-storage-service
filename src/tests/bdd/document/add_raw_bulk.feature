Feature: Add many documents in one request with the add-raw-bulk endpoint

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |
    Given there exist document with id "1" in data source "test-DS"
    """
    {
      "name": "root_package",
      "description": "",
      "type": "dmss://system/SIMOS/Package",
      "content": [],
      "isRoot": true
    }
    """

  Scenario: Every document in the batch is stored
    Given i access the resource url "/api/documents-add-raw-bulk/test-DS"
    When i make a "POST" request
    """
    [
      {"_id": "10", "name": "first", "type": "dmss://system/SIMOS/Package", "isRoot": false, "content": []},
      {"_id": "11", "name": "second", "type": "dmss://system/SIMOS/Package", "isRoot": false, "content": []}
    ]
    """
    Then the response status should be "OK"
    And the response should be
    """
    ["10", "11"]
    """

    Given i access the resource url "/api/documents/test-DS/$10"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {"_id": "10", "name": "first"}
    """

    Given i access the resource url "/api/documents/test-DS/$11"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {"_id": "11", "name": "second"}
    """

  Scenario: An existing document is replaced rather than duplicated
    Given i access the resource url "/api/documents-add-raw-bulk/test-DS"
    When i make a "POST" request
    """
    [{"_id": "1", "name": "renamed_root", "type": "dmss://system/SIMOS/Package", "isRoot": true, "content": []}]
    """
    Then the response status should be "OK"

    Given i access the resource url "/api/documents/test-DS/$1"
    When i make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {"_id": "1", "name": "renamed_root"}
    """

  Scenario: A document without an id is given a generated one
    Given i access the resource url "/api/documents-add-raw-bulk/test-DS"
    When i make a "POST" request
    """
    [{"name": "no_id_given", "type": "dmss://system/SIMOS/Package", "isRoot": false, "content": []}]
    """
    Then the response status should be "OK"
    And the length of the response should not be zero

  Scenario: An empty batch is accepted
    Given i access the resource url "/api/documents-add-raw-bulk/test-DS"
    When i make a "POST" request
    """
    []
    """
    Then the response status should be "OK"
    And the response should be
    """
    []
    """

  Scenario: A document is stored as-is, even without a type
    # The endpoint adds documents 'as-is' and does not validate them, matching /api/documents-add-raw.
    Given i access the resource url "/api/documents-add-raw-bulk/test-DS"
    When i make a "POST" request
    """
    [{"_id": "40", "name": "no_type_given"}]
    """
    Then the response status should be "OK"
    And the response should be
    """
    ["40"]
    """

  Scenario: A blueprint added in a batch can be used immediately
    # The use case only invalidates the blueprint cache when the batch contains a blueprint, so
    # validating against a blueprint that was just added pins that the invalidation happens.
    Given i access the resource url "/api/documents-add-raw-bulk/test-DS"
    When i make a "POST" request
    """
    [
      {
        "_id": "20",
        "name": "Box",
        "type": "dmss://system/SIMOS/Blueprint",
        "extends": ["dmss://system/SIMOS/NamedEntity"],
        "attributes": [
          {"name": "width", "type": "dmss://system/SIMOS/BlueprintAttribute", "attributeType": "integer"}
        ]
      },
      {
        "_id": "1",
        "name": "root_package",
        "type": "dmss://system/SIMOS/Package",
        "isRoot": true,
        "content": [
          {"address": "$20", "type": "dmss://system/SIMOS/Reference", "referenceType": "link"}
        ]
      }
    ]
    """
    Then the response status should be "OK"

    Given i access the resource url "/api/entity/validate"
    When i make a "POST" request
    """
    {"type": "dmss://test-DS/root_package/Box", "name": "aBox", "width": 600}
    """
    Then the response status should be "OK"

  Scenario: Overwriting a document the user may not write is refused
    # This endpoint writes many documents at once, so it must apply the same access control as
    # /api/documents-add-raw. Reaching past AuthorizedDataSource makes it an authorization bypass.
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "somebody",
      "others": "READ"
    }
    """
    Given the logged in user is "johndoe" with roles "a,b"
    Given authentication is enabled
    Given i access the resource url "/api/documents-add-raw-bulk/test-DS"
    When i make a "POST" request
    """
    [{"_id": "1", "name": "hijacked", "type": "dmss://system/SIMOS/Package", "isRoot": true, "content": []}]
    """
    Then the response status should be "Forbidden"
    And the response should contain
    """
    {
      "status": 403,
      "type": "MissingPrivilegeException"
    }
    """

  Scenario: A batch is refused unless the user may write every document in it
    Given AccessControlList for document "1" in data-source "test-DS" is
    """
    {
      "owner": "somebody",
      "others": "READ"
    }
    """
    Given the logged in user is "johndoe" with roles "a,b"
    Given authentication is enabled
    Given i access the resource url "/api/documents-add-raw-bulk/test-DS"
    When i make a "POST" request
    """
    [
      {"_id": "50", "name": "allowed", "type": "dmss://system/SIMOS/Package", "isRoot": false, "content": []},
      {"_id": "1", "name": "hijacked", "type": "dmss://system/SIMOS/Package", "isRoot": true, "content": []}
    ]
    """
    Then the response status should be "Forbidden"
