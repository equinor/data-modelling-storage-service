Feature: Exporting root packages
    Background: There are data sources in the system
    Given the system data source and SIMOS core package are available
    Given there are basic data sources with repositories
      |   name  |
      | test-DS |

    Given there are documents for the data source "test-DS" in collection "test-DS"
      | uid | parent_uid | name          | type                   |
      | 1   |            | blueprints    | dmss://system/SIMOS/Package   |
      | 2   | 1          | sub_package_1 | dmss://system/SIMOS/Package   |
      | 3   | 2          | document_1    | dmss://system/SIMOS/Blueprint |


  Scenario: A user want's to export a root package
    Given I access the resource url "/api/v1/export/test-DS/blueprints"
    When I make a "GET" request
    Then the response status should be "OK"
    And response node should not be empty
    And response should contain a zip file with name "dmt-export.zip"

