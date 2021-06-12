from behave import given
from services.database import data_source_collection
from storage.internal.data_source_repository import DataSourceRepository


@given("there are data sources")
def create_data_sources(context):
    for row in context.table:
        document = {"_id": row["name"], "name": row["name"]}
        data_source_collection.insert_one(document)


@given("there are repositories in the data sources")
def create_repositories(context):
    for row in context.table:
        document = {
            "data_types": row.get("dataTypes", "").split(","),
            "host": row["host"],
            "port": int(row["port"]),
            "username": row["username"],
            "password": row["password"],
            "tls": row["tls"],
            "database": row["database"],
            "collection": row["collection"],
            "type": row["type"],
        }
        DataSourceRepository.validate_repository(document)
        data_source_collection.update_one(
            {"_id": row["data-source"]}, {"$set": {f"repositories.{row['name']}": document}}
        )


@given("there are basic data sources with repositories")
def create_repositories(context):
    # First, add data sources
    for row in context.table:
        document = {"_id": row["name"], "name": row["name"]}
        data_source_collection.insert_one(document)

    # Then add repositories with default values to the data sources
    for row in context.table:
        document = {
            "data_types": ["default"],
            "host": "db",
            "port": 27017,
            "username": "maf",
            "password": "maf",
            "tls": "false",
            "database": "bdd-test",
            "collection": row["name"],
            "type": "mongo-db",
        }
        DataSourceRepository.validate_repository(document)
        data_source_collection.update_one({"_id": row["name"]}, {"$set": {f"repositories.{row['name']}": document}})
