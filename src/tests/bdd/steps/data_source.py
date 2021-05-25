from behave import given
from services.database import dmt_database


@given("there are data sources")
def create_data_sources(context):
    for row in context.table:
        document = {"_id": row["name"], "name": row["name"]}
        dmt_database["data_sources"].insert_one(document)


@given("there are repositories in the data sources")
def create_repositories(context):
    for row in context.table:
        document = {
            "dataTypes": row.get("dataTypes", "").split(","),
            "host": row["host"],
            "port": int(row["port"]),
            "username": row["username"],
            "password": row["password"],
            "tls": row["tls"],
            "database": row["database"],
            "collection": row["collection"],
            "type": row["type"],
        }

        dmt_database["data_sources"].update_one(
            {"_id": row["data-source"]}, {"$set": {f"repositories.{row['name']}": document}}
        )
        dmt_database.drop_collection(row["collection"])


@given("there are basic data sources with repositories")
def create_repositories(context):
    # First, add data sources
    for row in context.table:
        document = {"_id": row["name"], "name": row["name"]}
        dmt_database["data_sources"].insert_one(document)

    # Then add repositories with default values to the data sources
    for row in context.table:
        document = {
            "dataTypes": ["default"],
            "host": "db",
            "port": 27017,
            "username": "maf",
            "password": "maf",
            "tls": "false",
            "database": "local",
            "collection": row["name"],
            "type": "mongo-db",
        }

        dmt_database["data_sources"].update_one(
            {"_id": row["name"]}, {"$set": {f"repositories.{row['name']}": document}}
        )
        dmt_database.drop_collection(row["name"])
