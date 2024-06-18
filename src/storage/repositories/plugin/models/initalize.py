import os
import os.path
from plugin.models import Blueprint, Blueprints


def initialize_database(base_folder: str = None, api: str = None, run_migration=True):
    blueprints = Blueprints()
    if base_folder:
        for dirpath, dirnames, filenames in os.walk(base_folder):
            for filename in [f for f in filenames if f.endswith(".blueprint.json")]:
                blueprints.append(Blueprint.from_json(os.path.join(dirpath, filename[:-15])))

    elif api:
        # todo
        pass

    blueprints.generate_models()
    revision = blueprints.generate_migration_script()
    if run_migration:
        blueprints.upgrade(revision=revision)

