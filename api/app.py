import json
import os

import click
from flask import Flask

from config import Config
from core.domain.schema import Factory
from core.rest import DataSource, Document as DocumentBlueprint, Explorer, Index, System, Actions
from core.utility import wipe_db
from services.database import dmt_database
from utils.logging import logger
from utils.package_import import import_package


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(DocumentBlueprint.blueprint)
    app.register_blueprint(Explorer.blueprint)
    app.register_blueprint(DataSource.blueprint)
    app.register_blueprint(Index.blueprint)
    app.register_blueprint(System.blueprint)
    app.register_blueprint(Actions.blueprint)
    app.secret_key = os.urandom(64)
    return app


app = create_app(Config)


@app.cli.command()
def init_application():
    for folder in Config.SYSTEM_FOLDERS:
        import_package(f"{Config.APPLICATION_HOME}/core/{folder}", collection=Config.SYSTEM_COLLECTION, is_root=True)

    for folder in Config.ENTITY_APPLICATION_SETTINGS["packages"]:
        import_package(
            f"{Config.APPLICATION_HOME}/blueprints/{folder}", collection=Config.BLUEPRINT_COLLECTION, is_root=True
        )

    logger.info(f"Importing demo entity package(s) {Config.DEMO_ENTITIES}")
    for folder in Config.DEMO_ENTITIES:
        import_package(
            f"{Config.APPLICATION_HOME}/entities/{folder}", collection=Config.ENTITY_COLLECTION, is_root=True
        )
    logger.info("Resetting the cache of generated blueprints")
    Factory.reset_cache()


@app.cli.command()
def drop_data_sources():
    print(f"Dropping collection data_sources")
    dmt_database.drop_collection("data_sources")


@app.cli.command()
@click.argument("file")
def import_data_source(file):
    try:
        with open(file) as json_file:
            document = json.load(json_file)
            id = document["name"]
            document["_id"] = id
            print(f"Importing {file} as data_source with id: {id}.")
            dmt_database["data_sources"].replace_one({"_id": id}, document, upsert=True)
    except Exception as error:
        logger.error(f"Failed to import file {file}: {error}")


@app.cli.command()
def nuke_db():
    wipe_db()
