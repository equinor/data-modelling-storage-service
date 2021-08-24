import json
import time

import click
import uvicorn
from fastapi import APIRouter, FastAPI, Security
from starlette.requests import Request

from authentication.authentication import get_current_user
import authentication
from config import config
from controllers import (
    blob_controller,
    blueprint_controller,
    datasource_controller,
    document_controller,
    explorer_controller,
    export_controller,
    package_controller,
    reference_controller,
    search_controller,
    whoami_controller,
    healtcheck_controller,
    access_control_controller,
)
from restful.request_types.create_data_source import DataSourceRequest
from storage.internal.data_source_repository import DataSourceRepository
from utils.encryption import generate_key
from utils.logging import logger
from utils.package_import import import_package
from utils.wipe_db import wipe_db

server_root = "/api"
version = "v1"
prefix = f"{server_root}/{version}"
app = FastAPI(
    title="Data Modelling Storage Service",
    description="API for basic data modelling interaction",
    swagger_ui_init_oauth={"usePkceWithAuthorizationCodeGrant": True, "clientId": config.OAUTH_CLIENT_ID},
)

public_routes = APIRouter()
authenticated_routes = APIRouter()

public_routes.include_router(healtcheck_controller.router)

authenticated_routes.include_router(whoami_controller.router)
authenticated_routes.include_router(blob_controller.router)
authenticated_routes.include_router(datasource_controller.router)
authenticated_routes.include_router(document_controller.router)
authenticated_routes.include_router(export_controller.router)
authenticated_routes.include_router(package_controller.router)
authenticated_routes.include_router(search_controller.router)
authenticated_routes.include_router(blueprint_controller.router)
authenticated_routes.include_router(reference_controller.router)
authenticated_routes.include_router(explorer_controller.router)
authenticated_routes.include_router(access_control_controller.router)

app.include_router(authenticated_routes, prefix=prefix, dependencies=[Security(get_current_user)])
app.include_router(public_routes, prefix=prefix)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    milliseconds = int(round(process_time * 1000))
    logger.debug(f"Took \t{milliseconds}ms to process request '{request.url.path}'")
    return response


# TODO: Should probably look into other ways to handle user_context...
@app.middleware("http")
async def unset_user_context(request: Request, call_next):
    response = await call_next(request)
    authentication.user_context = None
    return response


@click.group()
def cli():
    pass


@cli.command()
def run():
    try:
        with open("./version.txt") as version_file:
            print(f"VERSION: {version_file.read()}")
    except FileNotFoundError:
        pass
    uvicorn.run(
        "app:app",
        host="0.0.0.0",  # nosec
        port=5000,
        reload=config.ENVIRONMENT == "local",
        log_level=config.LOGGER_LEVEL.lower(),
    )


@cli.command()
def init_application():
    logger.info("IMPORTING CORE DOCUMENTS")
    import_package(f"{config.APPLICATION_HOME}/system/SIMOS", data_source=config.CORE_DATA_SOURCE, is_root=True)
    logger.debug("DONE")


@cli.command()
@click.argument("file")
def import_data_source(file):
    with open(file) as json_file:
        document = json.load(json_file)
        DataSourceRepository().create(document["name"], DataSourceRequest(**document))


@cli.command()
def nuke_db():
    logger.info("PURGING DATABASE")
    wipe_db()
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
