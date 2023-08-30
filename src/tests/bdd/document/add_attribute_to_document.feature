Feature: Add attribute to document

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
                "address": "$StudyEntityId",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "storage"
            },
            {
                "address": "$StudyBlueprintId",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "storage"
            },
            {
                "address": "$CaseBlueprintId",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "storage"
            },
            {
                "address": "$JobBlueprintId",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "storage"
            },
            {
                "address": "$JobHandlerBlueprintId",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "storage"
            },
            {
                "address": "$SignalGeneratorJobBlueprintId",
                "type": "dmss://system/SIMOS/Reference",
                "referenceType": "storage"
            }
          ]
      }
      """

    Given there exist document with id "StudyBlueprintId" in data source "data-source-name"
      """
      {
        "name": "Study",
        "type": "dmss://system/SIMOS/Blueprint",
        "description": "",
        "attributes": [
          {
            "name": "type",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "string"
          },
          {
            "name": "cases",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "label": "Cases",
            "attributeType": "dmss://data-source-name/root_package/Case",
            "dimensions": "*",
            "contained": true
          }
        ]
      }
      """
      
    Given there exist document with id "CaseBlueprintId" in data source "data-source-name"
      """
      {
        "name": "Case",
        "type": "dmss://system/SIMOS/Blueprint",
        "description": "",
        "extends": [
          "dmss://system/SIMOS/NamedEntity"
        ],
        "attributes": [
          {
            "name": "duration",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "number"
          },
          {
            "name": "timeStep",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "number"
          },
          {
            "name": "job",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "dmss://data-source-name/root_package/Job",
            "optional": true
          }
        ]
      }

      """
    Given there exist document with id "JobBlueprintId" in data source "data-source-name"
      """
            {
        "name": "Job",
        "abstract": true,
        "type": "dmss://system/SIMOS/Blueprint",
        "attributes": [
          {
            "name": "type",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "string"
          },{
            "name": "outputTarget",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "string",
            "optional": true
          },
          {
            "attributeType": "dmss://data-source-name/root_package/JobHandler",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "name": "runner",
            "label": "Runner",
            "description": "JobRunner that will handle this job",
            "optional": true
          },
          {
            "attributeType": "object",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "name": "applicationInput",
            "label": "Input",
            "description": "Input entity to a job",
            "contained": false,
            "optional": true
          }
        ]
      }
      """
    Given there exist document with id "StudyEntityId" in data source "data-source-name"
      """
      {
        "_id": "StudyEntityId",
        "type": "dmss://data-source-name/root_package/Study",
        "name": "Simple-study-entity",
        "cases": [
          {
            "name": "case1",
            "type": "dmss://data-source-name/root_package/Case",
            "description": "",
            "duration": 100,
            "timeStep": 0.1
          }
        ]
      }
      """
    Given there exist document with id "JobHandlerBlueprintId" in data source "data-source-name"
      """
      {
        "type": "dmss://system/SIMOS/Blueprint",
        "name": "JobHandler",
        "description": "Base jobHandler type. Other jobHandlers should extend from this one",
        "attributes": [
              {
            "name": "type",
            "attributeType": "string",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "optional": false
          },
          {
            "attributeType": "string",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "name": "environmentVariables",
            "dimensions": "*",
            "optional": true,
            "description": "a list of strings on format 'myVar=myValue'"
          }
        ]
      }
      """
    Given there exist document with id "SignalGeneratorJobBlueprintId" in data source "data-source-name"
      """
      {
        "name": "SignalGeneratorJob",
        "type": "CORE:Blueprint",
        "description": "",
        "extends": [
          "dmss://data-source-name/root_package/JobHandler"
        ],
        "attributes": []
      }
      """
  Scenario: Add job to case
    Given i access the resource url "api/documents/data-source-name/$StudyEntityId.cases[0].job"
    When i make a form-data "POST" request
    """
    {
      "document": {
        "type": "dmss://data-source-name/root_package/Job",
        "applicationInput": {
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link",
          "address":
            "dmss://data-source-name/$StudyEntityId.cases[0]"
        },
        "runner": {
          "type": "dmss://data-source-name/root_package/SignalGeneratorJob"
        }
      }
    }
    """
    Then the response status should be "OK"

    Given i access the resource url "api/documents/data-source-name/$StudyEntityId.cases[0]"
    When i make a "GET" request
    Then the response should contain
    """
    {
      "name": "case1",
      "type": "dmss://data-source-name/root_package/Case",
      "description": "",
      "duration": 100,
      "timeStep": 0.1,
      "job": {
        "type": "dmss://data-source-name/root_package/Job",
        "applicationInput": {
          "type": "dmss://system/SIMOS/Reference",
          "referenceType": "link",
          "address":
            "dmss://data-source-name/$StudyEntityId.cases[0]"
        },
        "runner": {
          "type": "dmss://data-source-name/root_package/SignalGeneratorJob"
        }
      }
    }
    """
