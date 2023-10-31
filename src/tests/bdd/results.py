from terminaltables import AsciiTable

BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
ORANGE = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
ENDCOLOR = "\033[0m"


def colored_status(status, text):
    if status == "passed":
        return f"{GREEN}{text}{ENDCOLOR}"
    elif status == "skipped":
        return f"{BLUE}{text}{ENDCOLOR}"
    else:
        return f"{RED}{text}{ENDCOLOR}"


def two_decimals(number):
    return f"{number:.2f}"


def print_overview_features(features):
    table_data = [["Feature", "Scenario", "Duration"]]
    for feature in features:
        for scenario in feature.scenarios:
            table_data.append(
                [
                    feature.filename,
                    colored_status(scenario.status, scenario.name),
                    two_decimals(scenario.duration),
                ]
            )
    table = AsciiTable(table_data)
    print(table.table)


def print_overview_errors(errors):
    print("Errors: %s" % len(errors))

    for error in errors:
        table_data = [
            ["Feature", "Keyword", "Step", "Line"],
            [error.filename, error.keyword, error.name, str(error.line)],
        ]
        table = AsciiTable(table_data)
        print(table.table)
        # Need a line break to avoid overlapping tables and error messages
        print("\n")
        print(error.error_message)
