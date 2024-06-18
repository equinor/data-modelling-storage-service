from plugin.models import initialize_database
from plugin.crud import create_entity_from_file
from plugin.database import get_db_session
import os

#initialize_database
base_folder = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', "models"))
initialize_database(base_folder=base_folder)


# fill with data
session = get_db_session()
create_entity_from_file(db=session, filename=os.path.normpath(os.path.join(os.path.dirname(__file__), '..', "data", "study.json")))
create_entity_from_file(db=session, filename=os.path.normpath(os.path.join(os.path.dirname(__file__), '..', "data", "studyNC.json")))
