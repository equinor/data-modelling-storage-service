# Created by kristian at 26.04.2021Add to data source "test-source-name"
Feature: # Enter feature name here
  # Enter feature description here

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


    Given Add to data source "test-source-name"
    """
    RootPackages:
      TestData:
        id: 1
        content:
          itemType:
            id: 2
            type: system/SIMOS/Blueprint
            attributes:
              list:
                attributeType: string
                optional: true
              extra:
                attributeType: string
              complexList:
                dimensions: "*"
                optional: true
                attributeType: test-source-name/TestData/ItemTypeTwo
          ItemTypeTwo:
            id: 3
            type: system/SIMOS/Blueprint
            attributes:
              extra:
                attributeType: string
                optional: true
          TestContainer:
            id: 6
            type: system/SIMOS/Blueprint
            attributes:
              itemContained:
                optional: true
                attributeType: test-source-name/TestData/ItemType
              itemsContained:
                optional: true
                dimensions: "*"
                attributeType: test-source-name/TestData/ItemType
              itemNotContained:
                optional: false
                attributeType: test-source-name/TestData/ItemType
              itemsNotContained:
                optional: true,
                dimensions: "*"
                attributeType: test-source-name/TestData/ItemType

      TestData2:
        id: 4
        content:
          ItemType3:
            id: 5
            type: system/SIMOS/Blueprint
            attributes:
              power:
                attributeType: int
    """


  Scenario: # Enter scenario name here
