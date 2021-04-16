from pygments import highlight
import json

from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.data import JsonLexer

from utils.data_structure.traverse import traverse_compare


def print_pygments(json_object):
    json_str = json.dumps(json_object, indent=2, sort_keys=True)
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))


def pretty_eq(expected, actual):
    try:
        a = traverse_compare(expected, actual)
        b = []
        if a != b:
            print("Actual:")
            print_pygments(actual)
            print("Expected:")
            print_pygments(expected)
            print("Differences:")
            print_pygments(a)
        if a != b:
            raise Exception
    except KeyError:
        print_pygments(actual)
        raise Exception
    except IndexError:
        print_pygments(actual)
        raise Exception
    except Exception:
        raise Exception
