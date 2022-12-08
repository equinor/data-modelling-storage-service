Feature: Set logged in user as owner when creating an entity

    Background: There exist a document in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |

  Scenario: create entity with add_by_parent_id endpoint
      Given there exist document with id "2" in data source "test-DS"
      """
      {
          "name": "root_package",
          "description": "",
          "type": "dmss://system/SIMOS/Package",
          "isRoot": true,
          "content": []
      }
      """
      Given the logged in user is "johndoe" with roles "dmss-admin"
      Given authentication is enabled
      Given i access the resource url "/api/v1/documents/test-DS/2.content?update_uncontained=True"
      When i make a "POST" request
      """
      {
        "_id": "3",
        "name": "new_document",
        "type": "dmss://system/SIMOS/Blueprint"
      }
      """
      Then the response status should be "OK"
      And AccessControlList for document "3" in data-source "test-DS" should be
      """
      {
          "owner": "johndoe",
          "roles": {"dmss-admin": "WRITE"},
          "users": {},
          "others": "READ"
      }
      """


  Scenario: create entity with add_raw endpoint
      Given there exist document with id "2" in data source "test-DS"
      """
      {
          "name": "root_package",
          "description": "",
          "type": "dmss://system/SIMOS/Package",
          "isRoot": true,
          "content": []
      }
      """
      Given the logged in user is "johndoe" with roles "dmss-admin"
      Given authentication is enabled
      Given i access the resource url "/api/v1/documents/test-DS/add-raw"
      When i make a "POST" request
      """
      {
        "_id": "fe43f567-3606-41d7-972c-9800b8181846",
        "name": "new_document",
        "type": "dmss://system/SIMOS/Blueprint"
      }
      """
      Then the response status should be "OK"
      And AccessControlList for document "fe43f567-3606-41d7-972c-9800b8181846" in data-source "test-DS" should be
      """
      {
          "owner": "johndoe",
          "roles": {"dmss-admin": "WRITE"},
          "users": {},
          "others": "READ"
      }
      """