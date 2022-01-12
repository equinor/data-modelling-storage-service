Feature: Add document with document_service

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available

    Given there are data sources
      |       name         |
      | data-source-name   |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name       | database  | collection | type     | dataTypes    |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1      |  bdd-test | documents  | mongo-db | default      |

    Given there exist document with id "100" in data source "data-source-name"
      """
      {
          "name": "root_package",
          "description": "",
          "type": "system/SIMOS/Package",
          "isRoot": true,
          "content": [
              {
                  "_id": "1",
                  "name": "Comment",
                  "type": "system/SIMOS/Blueprint"
              },
              {
                  "_id": "2",
                  "name": "CommentList",
                  "type": "system/SIMOS/Blueprint"
              },
              {
                  "_id": "6",
                  "name": "Author",
                  "type": "system/SIMOS/Blueprint"
              },
              {
                  "_id": "101",
                  "type": "system/SIMOS/Package",
                  "name": "CommentsPackage"
              },
              {
                  "_id": "102",
                  "type": "system/SIMOS/Package",
                  "name": "EntityPackage"
              }
          ]
      }
      """

    Given there exist document with id "101" in data source "data-source-name"
      """
      {
          "name": "CommentsPackage",
          "description": "",
          "type": "system/SIMOS/Package",
          "isRoot": false,
          "content": [
              {
                  "_id": "3",
                  "type": "data-source-name/root_package/Comment",
                  "name": "comment1"
              },
              {
                  "_id": "4",
                  "type": "data-source-name/root_package/Comment",
                  "name": "comment2"
              }
          ]
      }
      """

    Given there exist document with id "102" in data source "data-source-name"
      """
      {
          "name": "EntityPackage",
          "description": "",
          "type": "system/SIMOS/Package",
          "isRoot": false,
          "content": [
                {
                  "_id": "5",
                  "name": "commentListEntity",
                  "type": "data-source-name/root_package/CommentList"
              }
          ]
      }
      """


    Given there exist document with id "1" in data source "data-source-name"
      """
      {
        "type": "system/SIMOS/Blueprint",
        "name": "Comment",
        "description": "",
        "extends": ["system/SIMOS/NamedEntity"],
        "attributes": [
          {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "text"
          },
          {
            "attributeType": "string",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "authors",
            "contained": true,
            "dimensions": "*"
          }
        ],
        "storageRecipes":[],
        "uiRecipes":[]
      }
      """

    Given there exist document with id "6" in data source "data-source-name"
      """
      {
        "type": "system/SIMOS/Blueprint",
        "name": "Author",
        "description": "Author blueprint",
        "extends": ["system/SIMOS/NamedEntity"],
        "attributes": [
          {
            "name": "books",
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "string",
            "dimensions": "*",
            "contained": true,
            "optional": false
          }
        ],
        "storageRecipes":[],
        "uiRecipes":[]
      }
      """


    Given there exist document with id "2" in data source "data-source-name"
      """
      {
        "type": "system/SIMOS/Blueprint",
        "name": "CommentList",
        "description": "A list of not contained comments",
        "extends": ["system/SIMOS/NamedEntity"],
        "attributes": [
          {
            "attributeType": "data-source-name/root_package/Comment",
            "type": "system/SIMOS/BlueprintAttribute",
            "name": "comments",
            "contained": false,
            "dimensions": "*"
          }
        ],
        "storageRecipes":[],
        "uiRecipes":[]
      }
      """
#must the comments attribute be nested?
    Given there exist document with id "3" in data source "data-source-name"
      """
      {
        "type": "data-source-name/root_package/Comment",
        "name": "comment1",
        "text": "an example comment with id 3",
        "authors": [
          {
            "name": "Per",
            "books": ["bookA", "BookB"],
            "type": "data-source-name/root_package/Author"
          },
          {
            "name": "Ole",
            "books": ["BookC", "BookD"],
            "type": "data-source-name/root_package/Author"
          }
       ]
      }
      """

    Given there exist document with id "4" in data source "data-source-name"
      """
      {
        "type": "data-source-name/root_package/Comment",
        "name": "comment2",
        "text": "an example comment with id 4",
        "authors": ["Hans", "Pål"]
      }
      """


    Given there exist document with id "5" in data source "data-source-name"
      """
      {
        "type": "data-source-name/root_package/CommentList",
        "name": "commentListEntity",
        "description": "",
        "comments": [
          {
            "_id": 3,
            "name": "comment1",
            "type": "data-source-name/root_package/Comment",
            "contained": false
          }
        ]
      }
      """

  Scenario: Add test
    Given i access the resource url "/api/v1/explorer/data-source-name/add-to-path"
    When i make a "POST" request with "1" files
    """
    {
      "directory": "/root_package/EntityPackage",
      "document":
      {
        "type": "data-source-name/root_package/CommentList",
        "name": "commentListEntity2",
        "description": "",
        "comments": []
      }
    }
    """
    Then the response status should be "OK"
#    And the response should equal
#    """
#    {
#      "type": "OK"
#    }
#    """


#    bug happens when:
#    i have an entity A that has a ref to anothe rentity B
#    when i use add() function to add an entity C, then B should NOT be updated-


