import json

from behave import when, given

from werkzeug.datastructures import FileStorage


def context_response_json(context):
    response = context.response
    # if response.status_code == 200 or response.status_code == 201:
    context.response_json = json.loads(response.data)


@given('i access the resource url "{url}"')
def step_access_url(context, url):
    context.url = str(url)


def get_headers(context):
    header = {}
    # Add authentication?
    return header


@when('i make a "{method}" request with "{number_of_files}" files')
def step_make_file_request(context, method, number_of_files):
    data = json.loads(context.text)
    # data["files"] = {}
    data["document"] = json.dumps(data["document"])
    if method == "POST":
        with open("api/tests_bdd/steps/test_pdf.pdf", "rb") as file:
            byte_file = FileStorage(file)
            for n in range(1, int(number_of_files) + 1):
                data[f"file{n}"] = byte_file
            context.response = context.repository.post(context.url, data=data, content_type="multipart/form-data")

    context.response_status = context.response.status_code
    if context.response.content_type == "application/json":
        context_response_json(context)


@when('i make a "{method}" request')
def step_make_request(context, method):
    data = {}
    if "text" in context and context.text:
        context.request_json = json.loads(context.text)
        data = json.dumps(context.request_json)

    headers = get_headers(context)

    if method == "PUT":
        context.response = context.repository.put(
            context.url, data=data, content_type="application/json", headers=headers
        )
    elif method == "POST":
        context.response = context.repository.post(
            context.url, data=data, content_type="application/json", headers=headers
        )
    elif method == "GET":
        context.response = context.repository.get(context.url, content_type="application/json", headers=headers)
    elif method == "DELETE":
        context.response = context.repository.delete(context.url, content_type="application/json", headers=headers)

    context.response_status = context.response.status_code
    if context.response.content_type == "application/json":
        context_response_json(context)
