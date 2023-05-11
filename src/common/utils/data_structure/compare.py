import json

from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.data import JsonLexer

from common.utils.data_structure.traverse import traverse_compare


def print_pygments(json_object):
    json_str = json.dumps(json_object, indent=2, sort_keys=True)
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))


def get_and_print_diff(actual: dict | list, expected: dict | list):
    diff = traverse_compare(actual, expected)
    if diff:
        print("Actual:")
        print_pygments(actual)
        print("Expected:")
        print_pygments(expected)
        print("Differences:")
        print_pygments(diff)
    return diff
