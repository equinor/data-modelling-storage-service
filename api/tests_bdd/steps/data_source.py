from behave import given
from api.services.database import dmt_database


@given("there are data sources")
def create_data_sources(context):
    for row in context.table:
        document = {"_id": row["name"], "name": row["name"]}
        dmt_database["data_sources"].insert_one(document)


@given("there are repositories in the data sources")
def create_repositories(context):
    context.repositories = {}
    for row in context.table:
        document = {
            "dataTypes": row.get("dataTypes", "").split(","),
            "host": row["host"],
            "port": int(row["port"]),
            "username": row["username"],
            "password": row["password"],
            "tls": row["tls"],
            "name": row["name"].strip(),
            "database": row["database"],
            "collection": row["collection"],
            "type": row["type"],
        }

        dmt_database["data_sources"].update_one(
            {"_id": row["data-source"]}, {"$set": {f"repositories.{row['name']}": document}}
        )
        dmt_database.drop_collection(row["collection"])
        context.repositories[row["name"]] = document
