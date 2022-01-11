Feature: Add document with document_service

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available

    Given there are data sources
      |       name         |
      | data-source-name   |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name       | database | collection | type     | dataTypes    |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1      |  bdd-test    | documents  | mongo-db | default      |

    Given there exist document with id "1" in data source "data-source-name"
      """
      {
        "type": "system/SIMOS/Blueprint",
        "name": "Comment",
        "description": "",
        "attributes": [
              {
                "text": "example comment",
                "type": "system/SIMOS/BlueprintAttribute",
                "attributeType": "string",
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
        "name": "HasReference",
        "description": "",
        "extends": ["system/SIMOS/NamedEntity"],
        "attributes": [
              {
                "name": "comments",
                "type": "system/SIMOS/BlueprintAttribute",
                "attributeType": "data-source-name/Comment",
                "contained": false,
                "dimensions": "*"
              }
        ],
        "storageRecipes":[],
        "uiRecipes":[]
      }
      """
#    Given there exist document with id "3" in data source "data-source-name"
#      """
#      {
#        "type": "system/SIMOS/Blueprint",
#        "name": "HasReference",
#        "description": "",
#        "extends": ["system/SIMOS/NamedEntity"],
#        "attributes": [
#              {
#                "name": "comments",
#                "type": "system/SIMOS/BlueprintAttribute",
#                "attributeType": "data-source-name/Comment",
#                "contained": false,
#                "dimensions": "*"
#              },
#        ],
#        "storageRecipes":[],
#        "uiRecipes":[]
#      }
#      """


  Scenario: Update document (only contained)
    Given i access the resource url "/api/v1/documents/data-source-name/2"



#    bug happens when:
#    i have an entity A that has a ref to anothe rentity B
#    when i use add() function to add an entity C, then B should NOT be updated-


