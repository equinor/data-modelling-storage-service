Feature: [test] generate package and blueprints in a simplified way 

  Background: There are data sources in the system

    Given there are data sources
      |       name         |
      | data-source-name   |
      | test-source-name   |
      | system             |

    Given there are repositories in the data sources
      | data-source      | host | port  | username | password | tls   | name       | database | collection | type     | dataTypes    |
      | data-source-name | db   | 27017 | maf      | maf      | false | repo1      | local    | documents  | mongo-db | default      |
      | test-source-name | db   | 27017 | maf      | maf      | false | blob-repo  | local    | blob-data  | mongo-db | default,blob |
      | data-source-name | db   | 27017 | maf      | maf      | false | doc-repo   | local    | test       | mongo-db | default      |
      | system           | db   | 27017 | maf      | maf      | false | system     | local    | system     | mongo-db | default      |



    #the goal is to replace the create packages with blueprints for the BDD tests in a simpler way.
    #I want to replace the the syntax used in the "Background" part of /bdd/document/crud.feature to create a package "TestData" that contains blueprints


    #this scenario tries to genearte the similar data as in the "Background" part of /bdd/document/crud.feature

  #Scenario: generate a test package with two blueprints
  #  Given there exists a package "TestData" with id "1" in data source "test-source-name"
  #  And the package "TestData" contains a bare minimum blueprint "ItemType" with id "2"
  #  And "ItemType" has an optional attribute "list" of type "string"
  #  And "ItemType" has an optional attribute "extra" of type "string"
  #  And "ItemType" has an optional array attribute "complexList" of type "string" with dimensions "*"
  #  And the package "TestData" contains a bare minimum blueprint "ItemTypeTwo" with id "3"
  #  And "ItemTypeTwo" has an optional attribute "extra" of type "string"


    
