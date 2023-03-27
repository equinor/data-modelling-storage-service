Feature: Update document that has blob data

  Background: There are data sources in the system
    Given the system data source and SIMOS core package are available

    Given there are data sources
      | name    |
      | test-DS |

    Given there are repositories in the data sources
      | data-source | host | port  | username | password | tls   | name       | database | collection | type     | dataTypes |
      | test-DS     | db   | 27017 | maf      | maf      | false | documents  | bdd-test | documents  | mongo-db | default   |
      | test-DS     | db   | 27017 | maf      | maf      | false | blob-repo  | bdd-test | blob-data  | mongo-db | blob      |


 Given there exist document with id "1" in data source "test-DS"
    """
    {
        "name": "root_package",
        "description": "",
        "type": "dmss://system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
               "type": "dmss://system/SIMOS/Link",
                "ref": "2",
                "targetName": "MultiplePdfContainer",
                "targetType": "dmss://system/SIMOS/Blueprint"
            },
            {
               "type": "dmss://system/SIMOS/Link",
                "ref": "3",
                "targetName": "new_pdf_container",
                "targetType": "dmss://test-DS/root_package/MultiplePdfContainer"
            }
        ]
    }
    """
    Given there exist document with id "2" in data source "test-DS"
    """
    {
      "type": "dmss://system/SIMOS/Blueprint",
      "name": "MultiplePdfContainer",
      "extends": ["dmss://system/SIMOS/NamedEntity"],
      "description": "A recursive blueprint with multiple PDFs",
      "attributes": [
        {
          "name": "a_pdf",
          "attributeType": "dmss://system/SIMOS/blob_types/PDF",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true
        },
        {
          "name": "another_pdf",
          "attributeType": "dmss://system/SIMOS/blob_types/PDF",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true
        },
        {
          "name": "pdf_container",
          "attributeType": "dmss://test-DS/root_package/MultiplePdfContainer",
          "type": "dmss://system/SIMOS/BlueprintAttribute",
          "optional": true
        }
      ]
    }
    """
    Given there exist document with id "3" in data source "test-DS"
    """
    {
        "name": "new_pdf_container",
        "type": "dmss://test-DS/root_package/MultiplePdfContainer",
        "a_pdf": {},
        "another_pdf": {},
        "pdf_container": {}
    }
    """

  Scenario: Update document with multiple blob entities
    Given i access the resource url "/api/documents/test-DS/3"
    When i make a "PUT" request with "4" files
    """
    {"data":{
        "name": "new_pdf_container",
        "type": "dmss://test-DS/root_package/MultiplePdfContainer",
        "a_pdf": {
          "name": "MyPDF1",
          "description": "",
          "type": "dmss://system/SIMOS/blob_types/PDF",
          "blob": {
            "name": "file1",
            "type": "dmss://system/SIMOS/Blob",
            "size": 0
          },
          "author": "Stig Oskar"
        },
        "another_pdf": {
          "name": "MyPDF2",
          "description": "",
          "type": "dmss://system/SIMOS/blob_types/PDF",
          "blob": {
            "name": "file2",
            "type": "dmss://system/SIMOS/Blob",
            "_blob_id": "",
            "size": 0
          },
          "author": "Stig Oskar"
        },
        "pdf_container": {
          "name": "second_pdf_container",
          "type": "dmss://test-DS/root_package/MultiplePdfContainer",
          "description": "",
          "a_pdf": {
            "name": "MyPDF3",
            "description": "",
            "type": "dmss://system/SIMOS/blob_types/PDF",
            "blob": {
              "name": "file3",
              "type": "dmss://system/SIMOS/Blob",
              "_blob_id": "",
              "size": 0
            },
            "author": "Stig Oskar"
          },
          "another_pdf": {
            "name": "MyPDF4",
            "description": "",
            "type": "dmss://system/SIMOS/blob_types/PDF",
            "blob": {
              "name": "file4",
              "type": "dmss://system/SIMOS/Blob",
              "_blob_id": "",
              "size": 0
            },
            "author": "Stig Oskar"
          },
          "pdf_container": {}
        }
    }}
    """
    Then the response status should be "OK"
