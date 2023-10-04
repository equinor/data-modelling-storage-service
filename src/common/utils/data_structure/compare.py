import json

from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.data import JsonLexer


def print_pygments(json_object):
    json_str = json.dumps(json_object, indent=2, sort_keys=True)
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))
