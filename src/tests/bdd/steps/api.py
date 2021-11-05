import json

from fastapi.testclient import TestClient
from behave import given, when, then

from domain_classes.user import User
from config import config
from auth_utils import generate_token


@given('i access the resource url "{url}"')
@then('i access the resource url "{url}"')
def step_access_url(context, url):
    from app import create_app

    context.url = str(url)
    context.test_client = TestClient(create_app())
    context.headers = {}
    if context.token:
        context.headers["Authorization"] = f"Bearer {context.token}"


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
def step_make_request(context, method):
    # These requests may contain files, so we use "multipart/form-data".
    # JSON must then be sent in the 'data' key part of the form
    if method == "PUT":
        context.response = context.test_client.put(context.url, data={"data": context.text}, headers=context.headers)
    elif method == "POST":
        context.response = context.test_client.post(context.url, data={"data": context.text}, headers=context.headers)
    else:
        raise Exception("A 'form-data' request must be either 'PUT' or 'POST'")


@when('i make a "{method}" request')
def step_make_request(context, method):
    if method == "PUT":
        context.response = context.test_client.put(context.url, json=json.loads(context.text), headers=context.headers)
    elif method == "POST":
        context.response = context.test_client.post(
            context.url, json=json.loads(context.text), headers=context.headers
        )
    elif method == "GET":
        context.response = context.test_client.get(context.url, headers=context.headers)
    elif method == "DELETE":
        context.response = context.test_client.delete(context.url, headers=context.headers)


@given('the logged in user is "{username}" with roles "{roles}"')
def step_set_access_token(context, username, roles):
    user = User(username=username, roles=roles.split(","))
    context.user = user
    context.token = generate_token(user)


@given("authentication is enabled")
def step_set_access_token(context):
    config.AUTH_ENABLED = True
