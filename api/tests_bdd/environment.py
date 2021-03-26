from api.config import Config
from api.core.utility import wipe_db
from api.services.database import dmt_database
from api.tests_bdd.results import print_overview_errors, print_overview_features
from fastapi.testclient import TestClient

from app import app

test_client = TestClient(app)


def before_all(context):
    context.errors = []
    context.features = []
    wipe_db()
    dmt_database.drop_collection(Config.DATA_SOURCES_COLLECTION)


def wipe_added_repositories(context):
    for repo in context.repositories.values():
        dmt_database.drop_collection(repo["collection"])


def after_all(context):
    print_overview_features(context.features)
    print_overview_errors(context.errors)


def after_feature(context, feature):
    if "skip" in feature.tags:
        feature.skip("Marked with @skip")
    context.features.append(feature)


def before_scenario(context, scenario):
    if "skip" in scenario.effective_tags:
        scenario.skip("Marked with @skip")

    context.test_client = test_client


def after_scenario(context, scenario):
    wipe_db()
    dmt_database.drop_collection(Config.DATA_SOURCES_COLLECTION)
    if "data_sources" in context:
        wipe_added_repositories(context)


def after_step(context, step):
    if step.status == "failed":
        context.errors.append(step)
