import re

from common.providers.address_resolver.path_items import (
    AttributeItem,
    IdItem,
    QueryItem,
)
from enums import SIMOS


def _next_path_part(path: str) -> tuple[str, str | None, str]:
    """Utility to get next path part."""
    content = path  # Default to path
    deliminator = None
    remaining_path = ""

    search = re.search(r"[.|/|\]|\[]", path)  # Search for next deliminator
    if search:
        deliminator = search.group(0)
        # Extract the content (the text between the two deliminators)
        content = path[: search.end() - 1]
        # Remove the extracted content (including deliminator), so that we don't handle it again.
        remaining_path = path[search.end() :]
    return content, deliminator, remaining_path


def path_to_path_items(path: str) -> list[AttributeItem | QueryItem | IdItem]:
    """Split up the path into path items.
    The path used as input to this function should not include protocol or data source.
    """
    queries = re.findall(r"\(([^\)]+)\)", path)
    if queries:
        # Split the path into the pieces surrounding the queries and remove trailing [( and )]
        remaining_ref_parts = re.split("|".join([re.escape(q) for q in queries]), path)
        remaining_ref_parts = [re.sub(r"\[?\($|^\)\]?", "", x) for x in remaining_ref_parts]

        items = _path_to_path_items(remaining_ref_parts[0], [], None)
        for index, query in enumerate(queries):
            items.append(QueryItem(query=query))
            items = _path_to_path_items(remaining_ref_parts[index + 1], [*items], None)
        return items
    else:
        return _path_to_path_items(path, [], None)


def _path_to_path_items(path: str, items, prev_deliminator) -> list[AttributeItem | QueryItem | IdItem]:
    if len(path) == 0:
        return items

    content, deliminator, remaining_path = _next_path_part(path)
    if content == "":
        # If the original path starts with a deliminator (e.g. /)
        # then there is no content.
        # The deliminator is extracted from the remaining path.
        # Continue resolve the remaining path.
        return _path_to_path_items(remaining_path, items, deliminator)

    if "$" in content:  # By id
        items.append(IdItem(content[1:]))
    elif len(items) == 0:  # By root package
        items.append(QueryItem(query=f"name={content},isRoot=True,type={SIMOS.PACKAGE.value}"))
    elif prev_deliminator == "/":  # By package
        items.append(AttributeItem("content"))
        items.append(QueryItem(query=f"name={content}"))
    elif prev_deliminator == "[" and deliminator == "]":  # By list index
        items.append(AttributeItem(f"[{content}]"))
    elif prev_deliminator == ".":  # By attribute
        items.append(AttributeItem(content))
    else:
        raise Exception(f"Not supported path format: {path}")

    return _path_to_path_items(remaining_path, items, deliminator)
