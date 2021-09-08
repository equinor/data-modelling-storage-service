import json

from behave import given, when, then

from authentication import authentication
from authentication.authentication import User
from config import config


@given('i access the resource url "{url}"')
@then('i access the resource url "{url}"')
def step_access_url(context, url):
    context.url = str(url)


@when('i make a "{method}" request with "{number_of_files}" files')
def step_make_file_request(context, method, number_of_files):
    # Parses the posted form-data. Converting everything to Dict[str, str]
    form_data = {k: json.dumps(v) if isinstance(v, dict) else str(v) for k, v in json.loads(context.text).items()}
    with open("tests/bdd/steps/test_pdf.pdf", "rb") as file:
        files = []
        for n in range(1, int(number_of_files) + 1):
            files.append(("files", (f"file{n}", file)))
        if method == "POST":
            context.response = context.test_client.post(context.url, data=form_data, files=files)
        if method == "PUT":
            context.response = context.test_client.put(context.url, data=form_data, files=files)


@when('i make a form-data "{method}" request')
def step_make_request(context, method):
    # These requests may contain files, so we use "multipart/form-data".
    # JSON must then be sent in the 'data' key part of the form
    if method == "PUT":
        context.response = context.test_client.put(context.url, data={"data": context.text})
    elif method == "POST":
        context.response = context.test_client.put(context.url, data={"data": context.text})
    else:
        raise Exception("A 'form-data' request must be either 'PUT' or 'POST'")


@when('i make a "{method}" request')
def step_make_request(context, method):
    if method == "PUT":
        context.response = context.test_client.put(context.url, json=json.loads(context.text))
    elif method == "POST":
        context.response = context.test_client.post(context.url, json=json.loads(context.text))
    elif method == "GET":
        context.response = context.test_client.get(context.url)
    elif method == "DELETE":
        context.response = context.test_client.delete(context.url)


@given('the logged in user is "{username}" with roles "{roles}"')
def step_set_access_token(context, username, roles):
    user = User(username=username, roles=roles.split(","))
    authentication.user_context = user


@given("authentication is enabled")
def step_set_access_token(context):
    config.AUTH_ENABLED = True
