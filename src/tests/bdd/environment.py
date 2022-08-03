from authentication.models import User

from tests.bdd.results import print_overview_errors, print_overview_features
from common.utils.wipe_db import wipe_db
from config import config

test_user = User(**{"user_id": "behave-test", "full_name": "Behave Test", "email": "behave-test@example.com"})


def before_all(context):
    context.errors = []
    context.features = []
    config.TEST_TOKEN = True
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
    config.AUTH_ENABLED = False
    if "skip" in scenario.effective_tags:
        scenario.skip("Marked with @skip")
    context.user = test_user


def after_step(context, step):
    if step.status == "failed":
        context.errors.append(step)
