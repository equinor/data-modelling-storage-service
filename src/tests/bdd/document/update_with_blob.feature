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
        "type": "system/SIMOS/Package",
        "isRoot": true,
        "content": [
            {
                "_id": "2",
                "name": "MultiplePdfContainer",
                "type": "system/SIMOS/Blueprint"
            },
            {
                "_id": "3",
                "name": "new_pdf_container",
                "type": "test-DS/root_package/MultiplePdfContainer"
            }
        ]
    }
    """
    Given there exist document with id "2" in data source "test-DS"
    """
    {
      "type": "system/SIMOS/Blueprint",
      "name": "MultiplePdfContainer",
      "extends": ["system/SIMOS/DefaultUiRecipes","system/SIMOS/NamedEntity"],
      "description": "A recursive blueprint with multiple PDFs",
      "attributes": [
        {
          "name": "a_pdf",
          "attributeType": "system/SIMOS/blob_types/PDF",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true
        },
        {
          "name": "another_pdf",
          "attributeType": "system/SIMOS/blob_types/PDF",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true
        },
        {
          "name": "pdf_container",
          "attributeType": "test-DS/root_package/MultiplePdfContainer",
          "type": "system/SIMOS/BlueprintAttribute",
          "optional": true
        }
      ]
    }
    """
    Given there exist document with id "3" in data source "test-DS"
    """
    {
        "name": "new_pdf_container",
        "type": "test-DS/root_package/MultiplePdfContainer",
        "a_pdf": {},
        "another_pdf": {},
        "pdf_container": {}
    }
    """

  Scenario: Update document with multiple blob entities
    Given i access the resource url "/api/v1/documents/test-DS/3"
    When i make a "PUT" request with "4" files
    """
    {"data":{
        "name": "new_pdf_container",
        "type": "test-DS/root_package/MultiplePdfContainer",
        "a_pdf": {
          "name": "MyPDF1",
          "description": "",
          "type": "system/SIMOS/blob_types/PDF",
          "blob": {
            "name": "file1",
            "type": "system/SIMOS/Blob",
            "size": 0
          },
          "author": "Stig Oskar"
        },
        "another_pdf": {
          "name": "MyPDF2",
          "description": "",
          "type": "system/SIMOS/blob_types/PDF",
          "blob": {
            "name": "file2",
            "type": "system/SIMOS/Blob",
            "_blob_id": "",
            "size": 0
          },
          "author": "Stig Oskar"
        },
        "pdf_container": {
          "name": "second_pdf_container",
          "type": "test-DS/root_package/MultiplePdfContainer",
          "description": "",
          "a_pdf": {
            "name": "MyPDF3",
            "description": "",
            "type": "system/SIMOS/blob_types/PDF",
            "blob": {
              "name": "file3",
              "type": "system/SIMOS/Blob",
              "_blob_id": "",
              "size": 0
            },
            "author": "Stig Oskar"
          },
          "another_pdf": {
            "name": "MyPDF4",
            "description": "",
            "type": "system/SIMOS/blob_types/PDF",
            "blob": {
              "name": "file4",
              "type": "system/SIMOS/Blob",
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
