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
                  "_id": "2",
                  "name": "Operation",
                  "type": "system/SIMOS/Blueprint"
              },
              {
                  "_id": "3",
                  "name": "Phase",
                  "type": "system/SIMOS/Blueprint"
              },
              {
                  "_id": "6",
                  "name": "VariableRun",
                  "type": "system/SIMOS/Blueprint"
              },
              {
                  "_id": "5",
                  "name": "ResultFile",
                  "type": "system/SIMOS/Blueprint"
              },
              {
                  "_id": "101",
                  "type": "system/SIMOS/Package",
                  "name": "Results"
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
          "name": "Results",
          "description": "",
          "type": "system/SIMOS/Package",
          "isRoot": false,
          "content": [
            {
                  "_id": "99",
                  "type": "data-source-name/root_package/Operation",
                  "name": "VisundEnsembleResults_2019090100"
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
                  "_id": "11",
                  "type": "data-source-name/root_package/Operation",
                  "name": "SverdrupAnchorReplace2021"
              }
          ]
      }
      """

    Given there exist document with id "2" in data source "data-source-name"
      """
      {
        "type": "system/SIMOS/Blueprint",
        "name": "Operation",
          "extends": ["system/SIMOS/DefaultUiRecipes", "system/SIMOS/NamedEntity"],
        "attributes": [
          {
            "name": "phases",
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "data-source-name/root_package/Phase",
            "contained": true,
            "dimensions": "*"
          }
        ],
        "storageRecipes":[],
        "uiRecipes":[]
      }
      """

    Given there exist document with id "3" in data source "data-source-name"
      """
      {
        "name": "Phase",
        "type": "system/SIMOS/Blueprint",
        "extends": ["system/SIMOS/DefaultUiRecipes", "system/SIMOS/NamedEntity"],
        "description": "A phase belonging to an Operation",
        "attributes": [
          {
            "name": "results",
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "data-source-name/root_package/ResultFile",
            "optional": true,
            "contained": false,
            "dimensions": "*"
          }
        ]
      }
      """


    Given there exist document with id "5" in data source "data-source-name"
      """
        {
          "name": "ResultFile",
          "type": "system/SIMOS/Blueprint",
          "extends": ["system/SIMOS/NamedEntity"],
          "attributes": [
            {
              "name": "variableRuns",
              "type": "system/SIMOS/BlueprintAttribute",
              "attributeType": "data-source-name/root_package/VariableRun",
              "dimensions": "*",
              "contained": true,
              "optional": false,
              "description": "Results relating to a set of variables"
            }
          ]
        }
      """


    Given there exist document with id "6" in data source "data-source-name"
      """
        {
          "name": "VariableRun",
          "type": "system/SIMOS/Blueprint",
          "description": "Results from a simulation corresponding to a set of key:value variables (\"no variations\")",
          "extends": ["system/SIMOS/NamedEntity"],
          "attributes": [
            {
              "name": "responses",
              "type": "system/SIMOS/BlueprintAttribute",
              "attributeType": "string",
              "dimensions": "*",
              "contained": true,
              "optional": false
            }
          ]
        }
      """


    Given there exist document with id "11" in data source "data-source-name"
      """
        {
          "_id": "11",
          "name": "SverdrupAnchorReplace2021",
          "type": "data-source-name/root_package/Operation",
          "description": "Bridge forecast",
          "phases": [
            {
              "name": "the-first_phase",
              "type": "data-source-name/root_package/Phase",
               "results": [
                    {
                      "type": "data-source-name/root_package/ResultFile",
                      "_id": "99",
                      "name": "result_weather_data"
                    }
              ]
            }
          ]
        }
      """

    Given there exist document with id "99" in data source "data-source-name"
      """
      {
        "_id": "99",
        "type": "data-source-name/root_package/ResultFile",
        "name": "VisundEnsembleResults_2019090100",
        "description": "Results",
        "variableRuns": [
          {
            "type": "data-source-name/root_package/VariableRun",
            "name": "VariableRun1",
            "responses": [
              "a", "b", "c"
            ]
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
        "type": "data-source-name/root_package/Operation",
        "name": "op",
        "description": "",
        "phases": []
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


























