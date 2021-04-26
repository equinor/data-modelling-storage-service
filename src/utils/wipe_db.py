from services.database import dmt_database


def wipe_db():
    print("Dropping all collections")
    # FIXME: Read names from the database
    for name in dmt_database.list_collection_names():
        print(f"Dropping collection '{name}'")
        dmt_database.drop_collection(name)
