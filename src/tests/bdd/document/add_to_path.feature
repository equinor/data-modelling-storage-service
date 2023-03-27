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
          "type": "dmss://system/SIMOS/Package",
          "isRoot": true,
          "content": [
              {
                  "ref": "2",
                  "type": "dmss://system/SIMOS/Link",
                  "targetName": "Operation",
                  "targetType": "dmss://system/SIMOS/Blueprint"
              },
              {
                  "ref": "3",
                  "type": "dmss://system/SIMOS/Link",
                  "targetName": "Phase",
                  "targetType": "dmss://system/SIMOS/Blueprint"
              },
              {
                  "ref": "6",
                  "type": "dmss://system/SIMOS/Link",
                  "targetName": "ResponseContainer",
                  "targetType": "dmss://system/SIMOS/Blueprint"
              },
              {
                  "ref": "5",
                  "type": "dmss://system/SIMOS/Link",
                  "targetName": "ResultFile",
                  "targetType": "dmss://system/SIMOS/Blueprint"
              },
              {
                  "ref": "101",
                  "type": "dmss://system/SIMOS/Link",
                  "targetName": "Results",
                  "targetType": "dmss://system/SIMOS/Package"
              },
              {
                  "ref": "102",
                  "type": "dmss://system/SIMOS/Link",
                  "targetName": "EntityPackage",
                  "targetType": "dmss://system/SIMOS/Package"
              }
          ]
      }
      """

    Given there exist document with id "101" in data source "data-source-name"
      """
      {
          "name": "Results",
          "description": "",
          "type": "dmss://system/SIMOS/Package",
          "isRoot": false,
          "content": [
            {
                  "ref": "99",
                  "type": "dmss://system/SIMOS/Link",
                  "targetType": "dmss://data-source-name/root_package/Operation",
                  "targetName": "result1"
            }
          ]
      }
      """

    Given there exist document with id "102" in data source "data-source-name"
      """
      {
          "name": "OperationPackage",
          "name": "OperationPackage",
          "description": "",
          "type": "dmss://system/SIMOS/Package",
          "isRoot": false,
          "content": [
              {
                  "ref": "11",
                  "type": "dmss://system/SIMOS/Link",
                  "targetType": "dmss://data-source-name/root_package/Operation",
                  "targetName": "operation1"
              }
          ]
      }
      """

    Given there exist document with id "2" in data source "data-source-name"
      """
      {
        "type": "dmss://system/SIMOS/Blueprint",
        "name": "Operation",
        "extends": ["dmss://system/SIMOS/NamedEntity"],
        "attributes": [
          {
            "name": "phases",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
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
        "type": "dmss://system/SIMOS/Blueprint",
        "extends": ["dmss://system/SIMOS/NamedEntity"],
        "attributes": [
          {
            "name": "results",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
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
          "type": "dmss://system/SIMOS/Blueprint",
          "extends": ["dmss://system/SIMOS/NamedEntity"],
          "attributes": [
            {
              "name": "responseContainer",
              "type": "dmss://system/SIMOS/BlueprintAttribute",
              "attributeType": "dmss://data-source-name/root_package/ResponseContainer",
              "contained": true,
              "optional": false
            }
          ]
        }
      """


    Given there exist document with id "6" in data source "data-source-name"
      """
        {
          "name": "ResponseContainer",
          "type": "dmss://system/SIMOS/Blueprint",
          "extends": ["dmss://system/SIMOS/NamedEntity"],
          "attributes": [
            {
              "name": "responses",
              "type": "dmss://system/SIMOS/BlueprintAttribute",
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
          "name": "operation1",
          "type": "dmss://data-source-name/root_package/Operation",
          "phases": [
            {
              "name": "the-first_phase",
              "type": "dmss://data-source-name/root_package/Phase",
               "results": [
                    {
                      "type": "dmss://data-source-name/root_package/ResultFile",
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
        "type": "dmss://data-source-name/root_package/ResultFile",
        "name": "result1",
        "description": "Results",
        "responseContainer":
          {
            "type": "dmss://data-source-name/root_package/ResponseContainer",
            "name": "response_container",
            "responses": [
              "responseA", "responseB", "responseC"
            ]
          }
      }
      """


  Scenario: Add test
    Given i access the resource url "/api/documents-by-path/data-source-name/root_package/EntityPackage"
    When i make a "POST" request with "1" files
    """
    {
      "document":
      {
        "type": "dmss://data-source-name/root_package/Operation",
        "name": "operation2",
        "description": "",
        "phases": []
      }
    }
    """
    Then the response status should be "OK"
    Given i access the resource url "/api/documents/data-source-name/99"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should equal
    """
      {
        "_id": "99",
        "type": "dmss://data-source-name/root_package/ResultFile",
        "name": "result1",
        "description": "Results",
        "responseContainer":
          {
            "type": "dmss://data-source-name/root_package/ResponseContainer",
            "name": "response_container",
            "responses": [
              "responseA", "responseB", "responseC"
            ]
          }
      }
    """

  Scenario: Add root package
    Given i access the resource url "/api/documents-by-path/data-source-name"
    When i make a form-data "POST" request
    """
    {
      "document":
      {
        "type": "dmss://system/SIMOS/Package",
        "name": "newRootPackage",
        "isRoot": true,
        "content": []
      }
    }
    """
    Then the response status should be "OK"
