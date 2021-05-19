import json

import click
import uvicorn
from fastapi import FastAPI


from config import Config
from services.database import dmt_database
from utils.logging import logger
from utils.package_import import import_blob, import_package
from controllers import (
    blob_controller,
    blueprint_controller,
    datasource_controller,
    document_controller,
    explorer_controller,
    package_controller,
    search_controller,
    reference_controller,
)
from utils.wipe_db import wipe_db

server_root = "/api"
version = "v1"
prefix = f"{server_root}/{version}"
app = FastAPI(title="Data Modelling Storage Service", description="API for basic data modelling interaction")
app.include_router(blob_controller.router, prefix=prefix)
app.include_router(datasource_controller.router, prefix=prefix)
app.include_router(document_controller.router, prefix=prefix)
app.include_router(explorer_controller.router, prefix=prefix)
app.include_router(package_controller.router, prefix=prefix)
app.include_router(search_controller.router, prefix=prefix)
app.include_router(blueprint_controller.router, prefix=prefix)
app.include_router(reference_controller.router, prefix=prefix)


@click.group()
def cli():
    pass


@cli.command()
def run():
    uvicorn.run(
        "app:app",
        host="0.0.0.0",  # nosec
        port=5000,
        reload=Config.ENVIRONMENT == "local",
        log_level=Config.LOGGER_LEVEL.lower(),
    )


@cli.command()
def init_application():
    logger.info("-------------- IMPORTING DEMO FILES ----------------")
    for folder in Config.SYSTEM_FOLDERS:
        import_package(
            f"{Config.APPLICATION_HOME}/system/{folder}", data_source=Config.SYSTEM_COLLECTION, is_root=True
        )

    logger.info(f"Importing demo package(s) {Config.ENTITY_APPLICATION_SETTINGS['packages']}")
    for folder in Config.ENTITY_APPLICATION_SETTINGS["packages"]:
        import_package(f"{Config.APPLICATION_HOME}/{folder}", data_source=Config.DEMO_DATASOURCE, is_root=True)

    for path in Config.IMPORT_BLOBS:
        import_blob(path)
    logger.info("-------------- DONE ----------------")


@cli.command()
@click.argument("file")
def import_data_source(file):
    try:
        with open(file) as json_file:
            document = json.load(json_file)
            id = document["name"]
            document["_id"] = id
            logger.info(f"Importing {file} as data_source with id: {id}.")
            dmt_database[f"{Config.DATA_SOURCES_COLLECTION}"].replace_one({"_id": id}, document, upsert=True)
    except Exception as error:
        logger.error(f"Failed to import file {file}: {error}")


@cli.command()
def nuke_db():
    logger.info("---------- PURGING DATABASE --------")
    wipe_db()
    logger.info("-------------- DONE ----------------")


if __name__ == "__main__":
    cli()
