import json
import time
from typing import Callable

import click
import gridfs
import uvicorn
from fastapi import APIRouter, FastAPI, Security
from starlette.requests import Request
from starlette.responses import Response

from authentication.authentication import auth_w_jwt_or_pat, auth_with_jwt
from authentication.models import User
from services.database import mongo_client
from config import config
from restful.request_types.create_data_source import DataSourceRequest
from storage.internal.data_source_repository import DataSourceRepository
from common.utils.encryption import generate_key
from common.utils.logging import logger
from common.utils.package_import import import_package

server_root = "/api"
version = "v1"
prefix = f"{server_root}/{version}"


def create_app() -> FastAPI:
    from features.access_control import access_control_feature
    from features.blob import blob_feature
    from features.blueprint import blueprint_feature
    from features.datasource import datasource_feature
    from features.document import document_feature
    from features.explorer import explorer_feature
    from features.export import export_feature
    from features.health_check import health_check_feature
    from features.personal_access_token import personal_access_token_feature
    from features.reference import reference_feature
    from features.search import search_feature
    from features.whoami import whoami_feature

    public_routes = APIRouter()
    public_routes.include_router(health_check_feature.router)

    authenticated_routes = APIRouter()
    authenticated_routes.include_router(access_control_feature.router)
    authenticated_routes.include_router(blob_feature.router)
    authenticated_routes.include_router(blueprint_feature.router)
    authenticated_routes.include_router(datasource_feature.router)
    authenticated_routes.include_router(document_feature.router)
    authenticated_routes.include_router(explorer_feature.router)
    authenticated_routes.include_router(export_feature.router)
    authenticated_routes.include_router(reference_feature.router)
    authenticated_routes.include_router(search_feature.router)
    authenticated_routes.include_router(whoami_feature.router)

    # Some routes a PAT can not be used to authenticate. For example, to get new access tokens. That would be bad...
    jwt_only_routes = APIRouter()
    jwt_only_routes.include_router(personal_access_token_feature.router)

    app = FastAPI(
        title="Data Modelling Storage Service",
        description="API for basic data modelling interaction",
        swagger_ui_init_oauth={"usePkceWithAuthorizationCodeGrant": True, "clientId": config.OAUTH_CLIENT_ID},
    )
    app.include_router(authenticated_routes, prefix=prefix, dependencies=[Security(auth_w_jwt_or_pat)])
    app.include_router(jwt_only_routes, prefix=prefix, dependencies=[Security(auth_with_jwt)])
    app.include_router(public_routes, prefix=prefix)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        milliseconds = int(round(process_time * 1000))
        logger.debug(f"{request.method} {request.url.path} - {milliseconds}ms - {response.status_code}")
        response.headers["X-Process-Time"] = str(process_time)
        return response

    return app


@click.group()
def cli():
    pass


@cli.command()
def run():
    uvicorn.run(
        "app:create_app",
        host="0.0.0.0",  # nosec
        port=5000,
        reload=config.ENVIRONMENT == "local",
        log_level=config.LOGGER_LEVEL.lower(),
    )


@cli.command()
def init_application():
    logger.info("IMPORTING CORE DOCUMENTS")
    # Running commands locally sets the user_context to "DMSS_ADMIN"
    user = User(**{"user_id": config.DMSS_ADMIN, "full_name": "Local Admin", "email": "admin@example.com"})
    import_package(f"{config.APPLICATION_HOME}/system/SIMOS", user, data_source=config.CORE_DATA_SOURCE, is_root=True)
    logger.debug("DONE")


@cli.command()
@click.argument("file")
def import_data_source(file):
    with open(file) as json_file:
        document = json.load(json_file)
        # Running commands locally sets the user_context to "DMSS_ADMIN"
        user = User(**{"user_id": config.DMSS_ADMIN, "full_name": "Local Admin", "email": "admin@example.com"})
        DataSourceRepository(user).create(document["name"], DataSourceRequest(**document))


@cli.command()
def nuke_db():
    logger.info("EMPTYING DATABASES")
    databases = mongo_client.list_database_names()
    # Don't touch the mongo admin or local database
    databases = [databasename for databasename in databases if databasename not in ("admin", "local", "config")]
    logger.warning(f"Emptying databases {databases}")
    for db_name in databases:
        print(db_name)
        logger.debug(f"Deleting all documents from database '{db_name}' from the DMSS system MongoDB server")
        for collection in mongo_client[db_name].list_collection_names():
            mongo_client[db_name][collection].delete_many({})
        blob_handler = gridfs.GridFS(mongo_client[db_name])
        for filename in blob_handler.list():
            print(filename)
            blob_handler.delete(filename)
    logger.debug("DONE")


@cli.command()
@click.pass_context
def reset_app(context):
    context.invoke(nuke_db)
    logger.info("CREATING SYSTEM DATA SOURCE")
    context.invoke(import_data_source, file="/code/home/system/data_sources/system.json")
    logger.debug("DONE")
    context.invoke(init_application)


@cli.command()
@click.pass_context
def create_key(context):
    key = context.invoke(generate_key)
    print(key)


if __name__ == "__main__":
    cli()
