import json
import mimetypes
from pathlib import Path
from time import sleep

from behave import given, step, then, when
from fastapi.testclient import TestClient

from authentication.models import User
from config import config
from tests.test_helpers.mock_token_generator import generate_mock_token


@step('i access the resource url "{url}"')
def step_access_url(context, url):
    from app import create_app

    context.url = str(url)
    context.test_client = TestClient(create_app())
    if not (getattr(context, "headers", None)):
        context.headers = None


@when('i make a "{method}" request with "{number_of_files}" files')
def step_make_file_request(context, method, number_of_files):
    # Parses the posted form-data. Converting everything to Dict[str, str]
    form_data = {k: json.dumps(v) if isinstance(v, dict) else str(v) for k, v in json.loads(context.text).items()}
    with open("tests/bdd/steps/test_pdf.pdf", "rb") as file:
        files = []
        for n in range(1, int(number_of_files) + 1):
            files.append(("files", (f"file{n}", file)))
        if method == "POST":
            context.response = context.test_client.post(
                context.url, data=form_data, files=files, headers=context.headers
            )
        if method == "PUT":
            context.response = context.test_client.put(
                context.url, data=form_data, files=files, headers=context.headers
            )


@when('i make a form-data "{method}" request')
def step_make_form_data_request(context, method):
    # These requests may contain files, so we use "multipart/form-data".
    # JSON must then be sent in the 'data' key part of the form
    form_data = {
        k: json.dumps(v) if isinstance(v, dict) or isinstance(v, list) else str(v)
        for k, v in json.loads(context.text).items()
    }
    if method == "PUT":
        context.response = context.test_client.put(context.url, data=form_data, headers=context.headers)
    elif method == "POST":
        context.response = context.test_client.post(context.url, data=form_data, headers=context.headers)
    else:
        raise Exception("A 'form-data' request must be either 'PUT' or 'POST'")


@when('i make a "{method}" request')
def step_make_x_method_request(context, method):
    if method == "PUT":
        context.response = context.test_client.put(context.url, json=json.loads(context.text), headers=context.headers)
    elif method == "POST":
        json_data = json.loads(context.text) if context.text else None
        if "binary_file" in context:
            # These requests may contain files, so we use "multipart/form-data".
            # JSON must then be sent in the 'data' key part of the form
            form_data = {
                k: json.dumps(v) if isinstance(v, dict) or isinstance(v, list) else str(v) for k, v in json_data.items()
            }
            file_name = Path(context.binary_file.name).name
            mime_type: str| None = ""
            guess = mimetypes.guess_type(file_name)
            if guess:
                mime_type = guess[0]
            files = {"file": (file_name, context.binary_file, mime_type)}
            context.response = context.test_client.post(
                context.url, data=form_data, files=files, headers=context.headers
            )
        else:
            context.response = context.test_client.post(context.url, json=json_data, headers=context.headers)
    elif method == "GET":
        context.response = context.test_client.get(context.url, headers=context.headers)
    elif method == "DELETE":
        context.response = context.test_client.delete(context.url, headers=context.headers)


@given('adding a binary file "{path}" to the request')
def step_add_binary_file(context, path: str):
    try:
        context.binary_file = open(path, "rb")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"The file {path}, was not found. Make sure the working directory of the test are set to be the source root (./src)"
        )


@given('the logged in user is "{user_id}" with roles "{roles}"')
def step_set_access_token(context, user_id, roles):
    user = User(user_id=user_id, roles=roles.split(","))
    context.user = user
    context.headers = {"Authorization": f"Bearer {generate_mock_token(user)}"}


@then("the PAT is added to context")
def step_add_PAT_to_context(context):
    context.pat = context.response.text.strip('"')


@then("the PAT is added to headers")
def step_add_PAT_to_header(context):
    context.headers = {"Access-Key": context.pat}


@step("the user logout")
def step_user_logout(context):
    context.user = None
    context.headers.pop("Access-Key")
    context.headers.pop("Authorization")
    context.token = None
    context.pat = None


@given("authentication is enabled")
def step_auth_enabled(context):
    config.AUTH_ENABLED = True


@then("the PAT is expired")
def step_PAT_is_expired(context):
    sleep(2)  # Give the PAT some time to expire
    context.response = context.test_client.get("/api/whoami", headers=context.headers)
    assert context.response.status_code == 401


@step("the PAT is revoked")
def step_PAT_is_revoked(context):
    context.response = context.test_client.delete(
        f"api/token/{context.response.json()[0]['uuid']}", headers=context.headers
    )
