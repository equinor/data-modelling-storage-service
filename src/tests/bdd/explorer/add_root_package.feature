Feature: Explorer - Add Root Package

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available

    Given there are data sources
      | name             |
      | data-source-name |
      | blueprints       |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name      | database | collection     | type     | dataTypes |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1     | local    | documents      | mongo-db | default   |
      | demo-DS   | db   | 27017 | maf      | maf      | false | blob-repo | local    | demo-DS | mongo-db | default   |

  Scenario: Add root package
    Given i access the resource url "/api/v1/explorer/data-source-name/add-package"
    When i make a "POST" request
    """
    {
      "name": "new_root_package",
      "type": "system/SIMOS/Package"
    }
    """
    Then the response status should be "OK"
    And the response should contain
    """
    {
        "data":{
           "name":"new_root_package",
           "description":null,
           "type":"system/SIMOS/Package",
           "isRoot":true,
           "storageRecipes":[]
        }
    }
    """

  Scenario: Add root package with missing parameter name should fail
    Given i access the resource url "/api/v1/explorer/data-source-name/add-package"
    When i make a "POST" request
    """
    {
      "type": "system/SIMOS/Package"
    }
    """
    Then the response status should be "Unprocessable Entity"
    And the response should equal
    """
    {"detail": [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]}
    """
