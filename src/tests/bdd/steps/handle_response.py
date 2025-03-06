import json
import pprint

from behave import then
from deepdiff import DeepDiff
from dictdiffer import diff
from test_helpers.print_pygments import print_pygments

from common.entity.find import find

STATUS_CODES = {
    "OK": 200,
    "Created": 201,
    "No Content": 204,
    "Bad Request": 400,
    "Unprocessable Entity": 422,
    "Unauthorized": 401,
    "Forbidden": 403,
    "Not Found": 404,
    "Conflict": 409,
    "System Error": 500,
}


def pretty_print_should_contain_diff(expected: dict, actual: dict):
    result = list(diff(actual, expected))
    changes = [diff for diff in result if diff[0] == "change"]
    missing_in_expected = [
        diff for diff in result if diff[0] == "add"
    ]  # find what is included in "actual", but is not included in the "expected"
    if changes or missing_in_expected:
        for c in changes:
            location = c[1] if isinstance(c[1], str) else ".".join([str(v) for v in c[1]])
            print_pygments(
                {
                    "location": location,
                    "difference": {"actual": c[2][0], "expected": c[2][1]},
                }
            )
        for m in missing_in_expected:
            location = m[1] if isinstance(m[1], str) else ".".join([str(v) for v in m[1]])
            print_pygments({"location": location, "missing value from actual response": m[2]})
        raise ValueError("The response does not match the expected result")


@then('the response status should be "{status}"')
def step_response_status(context, status):
    if context.response.status_code != STATUS_CODES[status]:
        pp = pprint.PrettyPrinter(indent=2)
        pretty_print = f"\n Actual: \n {pp.pformat(context.response.status_code)} \n Expected: \n {pp.pformat(STATUS_CODES[status])}"
        print(pretty_print)
        print(context.response.json())
    assert context.response.status_code == STATUS_CODES[status]


@then("the response should equal")
def step_impl_equal(context):
    actual = context.response.json()
    data = context.text or context.data
    expected = json.loads(data)
    difference = list(diff(actual, expected))
    if difference:
        changes = [diff for diff in difference if diff[0] == "change"]
        for change in changes:
            location = change[1] if isinstance(change[1], str) else ".".join([str(v) for v in change[1]])
            print_pygments(
                {
                    "location": location,
                    "difference": {"actual": change[2][0], "expected": change[2][1]},
                }
            )
        missing = [diff for diff in difference if diff[0] == "add"]
        for m in missing:
            print_pygments({"missing": m[2]})
        raise ValueError("The response does not match the expected result")


@then("the response at {dot_path} should equal")
def step_impl_equal_dot_path(context, dot_path):
    actual = context.response.json()
    target = find(actual, dot_path.split("."))
    data = context.text or context.data
    expected = json.loads(data)
    result = DeepDiff(target, expected, ignore_order=True)
    if result != {}:
        print("Actual:", target)
        print("Expected:", expected)
    assert result == {}


@then("the response should contain")
def step_impl_contain(context):
    actual = context.response.json()
    data = context.text or context.data
    expected = json.loads(data)
    pretty_print_should_contain_diff(expected, actual)


@then("the response should contain and have an id")
def step_impl_contain_id(context):
    actual = context.response.json()
    data = context.text or context.data
    expected = json.loads(data)
    if "_id" not in actual.keys():
        raise ValueError("The response does not have a '_id' key")
    del actual["_id"]
    pretty_print_should_contain_diff(expected, actual)


@then("the array at {dot_path} should be of length {length}")
def step_impl_array_length(context, dot_path, length):
    actual = context.response.json()
    target = find(actual, dot_path.split("."))
    result = len(target) == int(length)
    if not result:
        print(f"array is of length {len(target)}")
        print("array:", target)
    assert result


@then("the response should be")
def step_impl_should_be(context):
    if "text/plain" in context.response.headers["content-type"]:
        actual = context.response.text
        data = context.text
        assert actual == data
    else:
        actual = context.response.json()
        data = context.text or context.data
        assert actual == json.loads(data)


@then("the length of the response should not be zero")
def step_impl(context):
    assert int(context.response.headers["content-length"]) != 0


@then("response node should not be empty")
def step_not_empty_response(context):
    response = context.response
    assert response.headers["content-type"] == "application/zip" and len(response.content) > 200


@then('response should contain a zip file with name "{filename}"')
def step_contain_zip_file_with_name(context, filename: str):
    response = context.response
    assert response.headers["Content-Disposition"] == f"attachment; filename={filename}"
