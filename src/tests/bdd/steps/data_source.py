from behave import given

from common.providers.blueprint_provider import default_blueprint_provider
from common.utils.encryption import encrypt
from restful.request_types.create_data_source import DataSourceRequest
from services.database import data_source_db
from storage.internal.data_source_repository import DataSourceRepository
from storage.internal.get_data_source_cached import get_data_source_cached


@given("there are data sources")
def create_data_sources(context):
    for row in context.table:
        document = {"_id": row["name"], "name": row["name"]}
        data_source_db.set(row["name"], document)

    get_data_source_cached.cache_clear()
    default_blueprint_provider.get_data_source_cached.cache_clear()


@given("there are repositories in the data sources")
def create_repositories(context):
    data_sources = {}
    for row in context.table:
        document = {
            "data_types": row.get("dataTypes", "").split(","),
            "host": row["host"],
            "port": int(row["port"]),
            "username": row["username"],
            "password": encrypt(row["password"]),
            "tls": row["tls"],
            "database": row["database"],
            "collection": row["collection"],
            "type": row["type"],
        }
        DataSourceRepository(context.user).validate_repository(document)
        if row["data-source"] not in data_sources:
            data_source = data_source_db.get(row["data-source"])
            if not data_source:
                data_sources[row["data-source"]] = {
                    "_id": row["data-source"],
                    "name": row["data-source"],
                    "repositories": {},
                }
            else:
                data_sources[row["data-source"]] = data_source
                data_sources[row["data-source"]]["repositories"] = {}
        data_source = data_sources[row["data-source"]]
        data_source["repositories"][row["name"]] = document
        data_sources[row["data-source"]] = data_source

    for data_source in data_sources.values():
        data_source_db.set(data_source["_id"], data_source)
    get_data_source_cached.cache_clear()
    default_blueprint_provider.get_data_source_cached.cache_clear()


@given("there are basic data sources with repositories")
def create_basic_repositories(context):
    # First, add data sources
    document = {}
    for row in context.table:
        document = {"_id": row["name"], "name": row["name"]}

    # Then add repositories with default values to the data sources
    repos = {}
    for row in context.table:
        repos[row["name"]] = {
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
    document["repositories"] = repos
    DataSourceRepository(context.user).create(document["name"], DataSourceRequest(**document))

    get_data_source_cached.cache_clear()
    default_blueprint_provider.get_data_source_cached.cache_clear()
