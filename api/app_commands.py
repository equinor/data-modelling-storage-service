import json
import click
from app import create_app
from api.config import Config
from api.core.utility import wipe_db
from api.services.database import dmt_database
from api.utils.logging import logger
from api.utils.package_import import import_blob, import_package

app = create_app(Config)


@app.cli.command()
def init_application():
    for folder in Config.SYSTEM_FOLDERS:
        import_package(f"{Config.APPLICATION_HOME}/core/{folder}", data_source=Config.SYSTEM_COLLECTION, is_root=True)

    for folder in Config.ENTITY_APPLICATION_SETTINGS["packages"]:
        import_package(
            f"{Config.APPLICATION_HOME}/blueprints/{folder}", data_source=Config.BLUEPRINT_COLLECTION, is_root=True
        )

    logger.info(f"Importing entity package(s) {Config.ENTITY_APPLICATION_SETTINGS['entities']}")
    for folder in Config.ENTITY_APPLICATION_SETTINGS["entities"]:
        import_package(
            f"{Config.APPLICATION_HOME}/entities/{folder}", data_source=Config.ENTITY_COLLECTION, is_root=True
        )
    for path in Config.IMPORT_BLOBS:
        import_blob(path)


@app.cli.command()
def reset_core_packages():
    logger.warning(f"Dropping {Config.SYSTEM_COLLECTION} collection ")
    dmt_database.drop_collection(f"{Config.SYSTEM_COLLECTION}")
    logger.warning("Importing core packages...")
    for folder in Config.SYSTEM_FOLDERS:
        import_package(f"{Config.APPLICATION_HOME}/core/{folder}", data_source=Config.SYSTEM_COLLECTION, is_root=True)


@app.cli.command()
def drop_data_sources():
    print("Dropping collection data_sources")
    dmt_database.drop_collection(f"{Config.DATA_SOURCES_COLLECTION}")


@app.cli.command()
@click.argument("file")
def import_data_source(file):
    try:
        with open(file) as json_file:
            document = json.load(json_file)
            id = document["name"]
            document["_id"] = id
            print(f"Importing {file} as data_source with id: {id}.")
            dmt_database[f"{Config.DATA_SOURCES_COLLECTION}"].replace_one({"_id": id}, document, upsert=True)
    except Exception as error:
        logger.error(f"Failed to import file {file}: {error}")


@app.cli.command()
def nuke_db():
    wipe_db()
