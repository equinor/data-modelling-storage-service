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
                  "_id": "4",
                  "name": "SimulationConfig",
                  "type": "system/SIMOS/Blueprint"
              },
              {
                  "_id": "6",
                  "name": "VariableRun",
                  "type": "system/SIMOS/Blueprint"
              },
              {
                  "_id": "7",
                  "name": "Response",
                  "type": "system/SIMOS/Blueprint"
              },
              {
                  "_id": "5",
                  "name": "ResultFile",
                  "type": "system/SIMOS/Blueprint"
              },
              {
                  "_id": "8",
                  "name": "Variable",
                  "type": "system/SIMOS/Blueprint"
              },
              {
                  "_id": "9",
                  "name": "Timeseries",
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
            "attributeType": "/Blueprints/Phase",
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
            "name": "simulationConfigs",
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "/SimulationConfig",
            "optional": true,
            "contained": true,
            "dimensions": "*"
          }
        ]
      }
      """

    Given there exist document with id "4" in data source "data-source-name"
      """
      {
        "name": "SimulationConfig",
        "type": "system/SIMOS/Blueprint",
        "extends": ["system/SIMOS/DefaultUiRecipes", "system/SIMOS/NamedEntity"],
        "description": "",
        "attributes": [
          {
            "name": "results",
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "ForecastDS/FoR-BP/Blueprints/ResultFile",
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
              "attributeType": "/Blueprints/VariableRun",
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
              "attributeType": "/Blueprints/Response",
              "dimensions": "*",
              "contained": true,
              "optional": false,
              "description": "a list of responses, where each response can have a number of timeseries which relate to its statistics e.g. mean response, max response etc..."
            }, {
              "name": "variables",
              "type": "system/SIMOS/BlueprintAttribute",
              "attributeType": "/Blueprints/Variable",
              "dimensions": "*",
              "contained": true,
              "optional": false
            }
          ]
        }
      """

    Given there exist document with id "7" in data source "data-source-name"
      """
        {
          "name": "Response",
          "type": "system/SIMOS/Blueprint",
          "abstract": false,
          "extends": ["system/SIMOS/NamedEntity"],
          "attributes": [
            {
              "name": "statistics",
              "type": "system/SIMOS/BlueprintAttribute",
              "attributeType": "/Blueprints/Timeseries",
              "dimensions": "*",
              "contained": true,
              "optional": false
            }
          ]
        }
      """

    Given there exist document with id "8" in data source "data-source-name"
      """
        {
          "name": "Variable",
          "type": "system/SIMOS/Blueprint",
          "extends": ["system/SIMOS/NamedEntity"],
          "attributes": [
            {
              "name": "value",
              "type": "system/SIMOS/BlueprintAttribute",
              "attributeType": "string"
            }, {
              "name": "valueType",
              "type": "system/SIMOS/BlueprintAttribute",
              "attributeType": "string"
            }, {
              "name": "unit",
              "type": "system/SIMOS/BlueprintAttribute",
              "attributeType": "string"
            }
          ]
        }
      """

    Given there exist document with id "9" in data source "data-source-name"
      """
        {
        "name": "Timeseries",
        "type": "system/SIMOS/Blueprint",
        "description": "Storage for a single response time series e.g. Significant wave height vs time",
        "abstract": false,
        "extends": ["system/SIMOS/NamedEntity"],
        "attributes": [
          {
            "name": "datetimes",
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "string",
            "description": "datetimes from Unix epoch \r\n(Jan 1st 1970 at 00:00:00 UTC)",
            "dimensions": "*"
          }, {
            "name": "values",
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "number",
            "description": "The value array corresponding to the datetimes",
            "dimensions": "*",
            "default": "0.0"
          }, {
            "name": "unit",
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "string",
            "description": "The unit of the values"
          }, {
            "name": "threshold",
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "/Blueprints/Threshold",
            "contained": true,
            "optional": true,
            "description": "Optional threshold"
          },
          {
            "name": "plotType",
            "type": "system/SIMOS/BlueprintAttribute",
            "attributeType": "string",
            "description": "shaded or line"
          }
        ],
        "storageRecipes": [],
        "uiRecipes": []
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
              "simulationConfigs": [
                {
                  "name": "test1",
                  "published": true,
                  "type": "data-source-name/root_package/SimulationConfig",
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
              {
                "type": "ForecastDS/FoR-BP/Blueprints/Response",
                "name": "+ offset",
                "description": "+ offset response of plaform",
                "statistics": [
                  {
                    "type": "ForecastDS/FoR-BP/Blueprints/Timeseries",
                    "name": "Expected",
                    "description": "Expected extreme",
                    "datetimes": [
                      "01/Sep/2019, 00:00:00",
                      "01/Sep/2019, 03:00:00"
                    ],
                    "values": [
                      6.417742799539584, 6.789986092789259, 6.770189696855955
                    ],
                    "unit": "m",
                    "plotType": "line"
                  },
                  {
                    "type": "ForecastDS/FoR-BP/Blueprints/Timeseries",
                    "name": "80% C.I.",
                    "description": "80% Confidence Interval",
                    "datetimes": [
                      "01/Sep/2019, 00:00:00",
                      "01/Sep/2019, 03:00:00",
                      "01/Sep/2019, 06:00:00"
                    ],
                    "values": [
                      5.876925161801572, 6.166649355668352, 6.179770036474876,
                      6.174929531340336, 8.64142226560707, 12.510345988177368
                    ],
                    "unit": "m",
                    "plotType": "shaded"
                  }
                ]
              },
              {
                "type": "ForecastDS/FoR-BP/Blueprints/Response",
                "name": "+ heave",
                "description": "+ heave response of plaform",
                "statistics": [
                  {
                    "type": "ForecastDS/FoR-BP/Blueprints/Timeseries",
                    "name": "Expected",
                    "description": "Expected extreme",
                    "datetimes": [
                      "01/Sep/2019, 00:00:00",
                      "01/Sep/2019, 03:00:00"
                    ],
                    "values": [
                      3.15987250795791, 3.3370207552911904, 3.230304232471385
                    ],
                    "unit": "m",
                    "plotType": "line"
                  }
                ]
              }
            ],
            "variables": [
              {
                "type": "ForecastDS/FoR-BP/Blueprints/Variable",
                "name": "timestamp",
                "description": "Timestamp for metocean file (to be deprecated when Metocean API comes)",
                "value": "2019090100",
                "valueType": "string",
                "unit": "-"
              },
              {
                "type": "ForecastDS/FoR-BP/Blueprints/Variable",
                "name": "simulationLength",
                "description": "duration of simulation in hours (excluding transient)",
                "value": "3.0",
                "valueType": "number",
                "unit": "hr"
              }
            ]
          },
          {
            "type": "ForecastDS/FoR-BP/Blueprints/VariableRun",
            "name": "VariableRun2",
            "responses": [
              {
                "type": "ForecastDS/FoR-BP/Blueprints/Response",
                "name": "+ offset",
                "description": "+ offset response of plaform",
                "statistics": [
                  {
                    "type": "ForecastDS/FoR-BP/Blueprints/Timeseries",
                    "name": "Expected",
                    "description": "Expected extreme",
                    "datetimes": [
                      "01/Sep/2019, 00:00:00",
                      "01/Sep/2019, 03:00:00"
                    ],
                    "values": [
                      7.062187193053438, 7.538325128987874, 7.472483029492444
                    ],
                    "unit": "m",
                    "plotType": "line"
                  }
                ]
              }
            ],
            "variables": [
              {
                "type": "ForecastDS/FoR-BP/Blueprints/Variable",
                "name": "timestamp",
                "description": "Timestamp for metocean file (to be deprecated when Metocean API comes)",
                "value": "2019090100",
                "valueType": "string",
                "unit": "-"
              },
              {
                "type": "ForecastDS/FoR-BP/Blueprints/Variable",
                "name": "simulationLength",
                "description": "duration of simulation in hours (excluding transient)",
                "value": "3.0",
                "valueType": "number",
                "unit": "hr"
              }
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


























