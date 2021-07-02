import json

from behave import when, given


@given('i access the resource url "{url}"')
def step_access_url(context, url):
    context.url = str(url)


@when('i make a "{method}" request with "{number_of_files}" files')
def step_make_file_request(context, method, number_of_files):
    data = json.loads(context.text)
    data["document"] = json.dumps(data["document"])
    if method == "POST":
        with open("tests/bdd/steps/test_pdf.pdf", "rb") as file:
            files = []
            for n in range(1, int(number_of_files) + 1):
                files.append(("files", (f"file{n}", file)))
            context.response = context.test_client.post(context.url, data=data, files=files)


@when('i make a "{method}" request')
def step_make_request(context, method):
    data = {}
    if "text" in context and context.text:
        data = json.loads(context.text)

    if method == "PUT":
        context.response = context.test_client.put(context.url, json=data)
    elif method == "POST":
        context.response = context.test_client.post(context.url, json=data)
    elif method == "GET":
        context.response = context.test_client.get(context.url)
    elif method == "DELETE":
        context.response = context.test_client.delete(context.url)
