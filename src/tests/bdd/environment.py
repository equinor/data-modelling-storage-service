from fastapi.testclient import TestClient

from app import app
from tests.bdd.results import print_overview_errors, print_overview_features
from utils.wipe_db import wipe_db

test_client = TestClient(app)


def before_all(context):
    context.errors = []
    context.features = []
    wipe_db()


def after_all(context):
    print_overview_features(context.features)
    print_overview_errors(context.errors)
    wipe_db()


def after_feature(context, feature):
    if "skip" in feature.tags:
        feature.skip("Marked with @skip")
    context.features.append(feature)


def before_scenario(context, scenario):
    wipe_db()
    if "skip" in scenario.effective_tags:
        scenario.skip("Marked with @skip")
    context.test_client = test_client


def after_step(context, step):
    if step.status == "failed":
        context.errors.append(step)
