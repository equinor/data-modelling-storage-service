from authentication.models import User
from common.providers.blueprint_provider import get_blueprint_provider
from config import config
from tests.bdd.results import print_overview_errors, print_overview_features
from tests.test_helpers.wipe_db import wipe_db

test_user = User(
    **{
        "user_id": "behave-test",
        "full_name": "Behave Test",
        "email": "behave-test@example.com",
    }
)


def before_all(context):
    context.errors = []
    context.features = []
    config.TEST_TOKEN = True
    wipe_db()


def after_all(context):
    print_overview_features(context.features)
    print_overview_errors(context.errors)


def after_feature(context, feature):
    if "skip" in feature.tags:
        feature.skip("Marked with @skip")
    context.features.append(feature)
    bp = get_blueprint_provider()
    bp.invalidate_cache()


def before_scenario(context, scenario):
    wipe_db()
    config.AUTH_ENABLED = False
    if "skip" in scenario.effective_tags:
        scenario.skip("Marked with @skip")
    context.user = test_user


def after_step(context, step):
    if step.status == "failed":
        context.errors.append(step)
