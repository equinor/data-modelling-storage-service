from config import Config
from services.database import dmt_database


def wipe_db():
    print("Dropping all collections")
    # FIXME: Read names from the database
    for name in [
        Config.BLUEPRINT_COLLECTION,
        Config.ENTITY_COLLECTION,
        Config.SYSTEM_COLLECTION,
        "documents",
        "fs.chunks",
        "fs.files",
    ]:
        print(f"Dropping collection '{name}'")
        dmt_database.drop_collection(name)
