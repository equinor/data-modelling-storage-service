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
                  "address": "$2",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
              },
              {
                  "address": "$3",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
              },
              {
                  "address": "$6",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
              },
              {
                  "address": "$5",
                  "type": "dmss://system/SIMOS/Reference",
                   "referenceType": "link"
              },
              {
                  "address": "$7",
                  "type": "dmss://system/SIMOS/Reference",
                   "referenceType": "link"
              },
              {
                  "address": "$101",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
              },
              {
                  "address": "$102",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
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
                  "address": "$99",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
            }
          ]
      }
      """

    Given there exist document with id "102" in data source "data-source-name"
      """
      {
          "name": "EntityPackage",
          "description": "",
          "type": "dmss://system/SIMOS/Package",
          "isRoot": false,
          "content": [
              {
                  "address": "$11",
                  "type": "dmss://system/SIMOS/Reference",
                  "referenceType": "link"
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
            "attributeType": "dmss://data-source-name/root_package/Phase",
            "contained": true,
            "dimensions": "*"
          }
        ]
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
            "attributeType": "dmss://data-source-name/root_package/ResultFile",
            "optional": true,
            "contained": false,
            "dimensions": "*"
          },
          {
            "name": "containedResults",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "dmss://data-source-name/root_package/ResultFile",
            "optional": true,
            "contained": true,
            "dimensions": "*"
          },
          {
            "name": "additionalInfo",
            "type": "dmss://system/SIMOS/BlueprintAttribute",
            "attributeType": "object",
            "optional": true
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

    Given there exist document with id "7" in data source "data-source-name"
      """
        {
        	"name": "PhaseInfo",
        	"type": "dmss://system/SIMOS/Blueprint",
        	"extends": ["dmss://system/SIMOS/NamedEntity"],
        	"attributes": [{
        		"name": "startDate",
        		"type": "dmss://system/SIMOS/BlueprintAttribute",
        		"attributeType": "string"
        	}]
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
                    "address": "$99",
                    "type": "dmss://system/SIMOS/Reference",
                    "referenceType": "link"
                    }
              ],
              "containedResults": []
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


  Scenario: Add document to EntityPackage using path as reference
    Given i access the resource url "/api/documents/data-source-name/root_package/EntityPackage"
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
    Given i access the resource url "/api/documents/data-source-name/root_package/EntityPackage/operation2?depth=2"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
      {
        "type": "dmss://data-source-name/root_package/Operation",
        "name": "operation2",
        "description": "",
        "phases": []
      }
    """

  Scenario: Add document to EntityPackage using id as reference
    Given i access the resource url "/api/documents/data-source-name/root_package.content[6]"
    When i make a "POST" request with "1" files
    """
    {
      "document":
      {
        "type": "dmss://data-source-name/root_package/Operation",
        "name": "operation3",
        "description": "",
        "phases": []
      }
    }
    """
    Then the response status should be "Bad Request"
    And the response should contain
    """
    {
      "status": 400, "type": "ValidationException",
      "message": "Entity should be of type 'dmss://system/SIMOS/Reference' (or extending from it). Got 'dmss://data-source-name/root_package/Operation'",
      "debug": "Location: Entity in key '^'",
      "data": {
        "description": "",
        "name": "operation3",
        "phases": [],
        "type": "dmss://data-source-name/root_package/Operation"
        }
    }
    """


  Scenario: Add document to root package using path as reference
    Given i access the resource url "/api/documents/data-source-name/root_package"
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
    Given i access the resource url "/api/documents/data-source-name/root_package/operation2?depth=2"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
      {
        "type": "dmss://data-source-name/root_package/Operation",
        "name": "operation2",
        "description": "",
        "phases": []
      }
    """


  Scenario: Add document to root package using id as reference
    Given i access the resource url "/api/documents/data-source-name/$100"
    When i make a "POST" request with "1" files
    """
    {
      "document":
      {
        "type": "dmss://data-source-name/root_package/Operation",
        "name": "operation3",
        "description": "",
        "phases": []
      }
    }
    """
    Then the response status should be "OK"
    Given i access the resource url "/api/documents/data-source-name/root_package.content[7]?depth=2"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
      {
        "type": "dmss://data-source-name/root_package/Operation",
        "name": "operation3",
        "description": "",
        "phases": []
      }
    """


  Scenario: Add root package
    Given i access the resource url "/api/documents/data-source-name"
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

  Scenario: add document to list using path
    Given i access the resource url "/api/documents/data-source-name/root_package/EntityPackage/operation1.phases"
    When I make a "POST" request with "1" files
    """
    {
      "document":
      {
          "name": "the-second-phase",
          "type": "dmss://data-source-name/root_package/Phase",
           "results": []
      }
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {"uid": "11.phases[1]"}
    """
    Given i access the resource url "/api/documents/data-source-name/root_package/EntityPackage/operation1?depth=3"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
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
              ]
            },
            {
            "name": "the-second-phase",
            "type": "dmss://data-source-name/root_package/Phase",
             "results": []
            }
          ]
        }
    """

  Scenario: add document to list using id
    Given i access the resource url "/api/documents/data-source-name/$11.phases[0].containedResults"
    When I make a "POST" request with "1" files
    """
    {
      "document":
       {
        "type": "dmss://data-source-name/root_package/ResultFile",
        "name": "addedResult",
        "description": "added result via document update",
        "responseContainer":
          {
            "type": "dmss://data-source-name/root_package/ResponseContainer",
            "name": "response_container",
            "responses": [
              "responseA", "responseB", "responseC"
            ]
          }
      }
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
      {
        "uid": "11.phases[0].containedResults[0]"
      }
    """
#     todo update document add use case such that id contains bracket notation for lists: 11.phases[0].containedResults[0]
    Given i access the resource url "/api/documents/data-source-name/$11.phases[0].containedResults?depth=2"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
        [
           {
            "type": "dmss://data-source-name/root_package/ResultFile",
            "name": "addedResult",
            "description": "added result via document update",
            "responseContainer":
              {
                "type": "dmss://data-source-name/root_package/ResponseContainer",
                "name": "response_container",
                "responses": [
                  "responseA", "responseB", "responseC"
                ]
              }
          }
        ]
    """

  Scenario: object
    Given i access the resource url "/api/documents/data-source-name/root_package/EntityPackage"
    When I make a "POST" request with "1" files
    """
    {
    	"document": {
    		"name": "new-phase",
    		"type": "dmss://data-source-name/root_package/Phase",
    		"results": [],
    		"containedResults": [],
    		"additionalInfo": {
    			"type": "dmss://data-source-name/root_package/PhaseInfo",
    			"name": "extra_info",
    			"startDate": "01.01.2000"
    		}
    	}
    }
    """
    Then the response status should be "OK"
    Given i access the resource url "/api/documents/data-source-name/root_package/EntityPackage/new-phase?depth=2"
    When I make a "GET" request
    Then the response status should be "OK"
    And the response should contain
    """
    {
    		"name": "new-phase",
    		"type": "dmss://data-source-name/root_package/Phase",
    		"results": [],
    		"containedResults": [],
    		"additionalInfo": {
    			"type": "dmss://data-source-name/root_package/PhaseInfo",
    			"name": "extra_info",
    			"startDate": "01.01.2000"
    		}
    	}
    """
