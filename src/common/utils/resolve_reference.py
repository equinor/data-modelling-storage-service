import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, Tuple, Union

from common.exceptions import ApplicationException, NotFoundException
from common.utils.data_structure.find import find
from common.utils.data_structure.is_same import is_same
from common.utils.is_reference import is_reference
from enums import Protocols
from storage.data_source_class import DataSource


def split_reference(reference: str) -> list[str]:
    """Splits a reference into it's string components
    e.g. "$123.content[1]" -> ["$123", ".content", "[1]"]"""
    parts = []
    remaining_ref = reference
    while remaining_ref:
        if remaining_ref[0] in "./":
            prefix_delim = remaining_ref[0]
            content = re.split(r"[./\[(]", remaining_ref, 2)[1]
            parts.append(f"{prefix_delim}{content}")
            remaining_ref = remaining_ref.removeprefix(parts[-1])
            continue
        if remaining_ref[0] in "[(":
            prefix_delim = remaining_ref[0]
            closing_bracket = "]" if prefix_delim == "[" else ")"
            content = re.split("[" + re.escape(f"{closing_bracket}") + "]", remaining_ref, 2)[0][1:]
            parts.append(f"{prefix_delim}{content}{closing_bracket}")
            remaining_ref = remaining_ref.removeprefix(parts[-1])
            continue

        content = re.split(r"[./]", remaining_ref, 1)[0]
        remaining_ref = remaining_ref.removeprefix(content)
        parts.append(content)
    return parts


def _next_reference_part(reference: str) -> Tuple[str, Union[str, None], str]:
    """Utility to get next reference part."""
    content = reference  # Default to reference
    deliminator = None
    remaining_reference = ""

    search = re.search(r"[.|/|\]|\[|(|)]", reference)  # Search for next deliminator
    if search:
        deliminator = search.group(0)
        # Extract the content (the text between the two deliminators)
        content = reference[: search.end() - 1]
        # Remove the extracted content (including deliminator), so that we don't handle it again.
        remaining_reference = reference[search.end() :]
    return content, deliminator, remaining_reference


@dataclass
class IdItem:
    """Points to an id."""

    id: str

    def get_entry_point(self, data_source: DataSource) -> Tuple[dict, str]:
        # Get the document from the data source
        result = data_source.get(self.id)
        if not result:
            raise NotFoundException(
                f"No document with id '{self.id}' could be found in data source '{data_source.name}'."
            )
        return result, self.id

    def __repr__(self):
        return f"${self.id}"


@dataclass
class QueryItem:
    """Query a list for a document."""

    query: str

    def filter(self) -> Dict[str, Any]:
        """Create filter from query string."""
        query: Dict[str, Any] = {}
        for pair in self.query.split(","):
            key, value = pair.split("=")
            if value == "True" or value == "False":
                query[key] = bool(value)
            else:
                query[key] = value
        return query

    def get_entry_point(self, data_source: DataSource) -> Tuple[dict, str]:
        result: list[dict] = data_source.find(self.filter())
        if not result:
            raise NotFoundException(
                f"No document that match '{self.query}' could be found in data source '{data_source.name}'."
            )
        if len(result) > 2:
            raise ApplicationException(
                f"More than 1 document that match '{self.query}' was returned from DataSource. That should not happen..."
            )
        return result[0], result[0]["_id"]

    def get_child(
        self, document: dict | list, data_source: DataSource, get_data_source: Callable, resolve: bool = False
    ) -> Tuple[Any, str]:
        # Search inside an existing document (need to resolve any references first before trying to compare against filter)
        elements = [
            resolve_reference(f"/{data_source.name}/{f['address']}", get_data_source, resolve).entity
            if is_reference(f)
            else f
            for f in document
        ]  # Resolve any references
        try:
            child, index = next(
                ((element, str(index)) for index, element in enumerate(elements) if is_same(element, self.filter())),
            )  # Find an item that match the given filter
            if resolve:
                return child, index
            return find(document, [f"[{index}]"]), f"[{index}]"
        except StopIteration:
            raise ApplicationException(f"No object matches filter '{self.query}'", data={"elements": elements})


@dataclass
class AttributeItem:
    """Move into a key of an object or find an item in a list based on index position."""

    path: str

    def __repr__(self):
        return self.path

    def get_child(
        self, document: dict | list, data_source: DataSource, get_data_source: Callable, resolve: bool = False
    ) -> tuple[Any, str]:
        if isinstance(document, dict) and is_reference(document):
            document = resolve_reference(f"/{data_source.name}/{document['address']}", get_data_source).entity
        try:
            result = find(document, [self.path])
        except (IndexError, ValueError, KeyError):
            if isinstance(document, dict):
                raise NotFoundException(
                    f"Invalid attribute '{self.path}'. Valid attributes are '{list(document.keys())}'."
                )
            else:
                raise NotFoundException(f"Invalid index '{self.path}'. Valid indices are < {len(document)}.")

        return result, self.path


def reference_to_reference_items(
    reference: str, items=None, prev_deliminator=None
) -> list[AttributeItem | QueryItem | IdItem]:
    """Split up the reference into reference items. DataSourceItem return as first element"""

    if len(reference) == 0:
        return items

    if not items:
        items = []

    content, deliminator, remaining_reference = _next_reference_part(reference)
    if content == "":
        # If the original reference starts with a deliminator (e.g. /)
        # or two deliminators are next to each other (e.g. ([),
        # then there is no content.
        # The deliminator is extracted from the remaining reference.
        # Continue resolve the remaining reference.
        return reference_to_reference_items(remaining_reference, items, deliminator)

    # TODO: Handle queries with paths, ex type=test_data/complex/Customer
    if "$" in content:  # By id
        items.append(IdItem(content[1:]))
    elif prev_deliminator == "/" and len(items) == 0:  # By root package
        items.append(QueryItem(query=f"name={content},isRoot=True"))
    elif prev_deliminator == "/":  # By package
        items.append(AttributeItem("content"))
        items.append(QueryItem(query=f"name={content}"))
    elif prev_deliminator == "(" and deliminator == ")":  # By query
        items.append(QueryItem(query=content))
    elif prev_deliminator == "[" and deliminator == "]":  # By list index
        items.append(AttributeItem(f"[{content}]"))
    elif prev_deliminator == ".":  # By attribute
        items.append(AttributeItem(content))
    else:
        raise Exception(f"Not supported reference format: {reference}")

    return reference_to_reference_items(remaining_reference, items, deliminator)


def split_data_source_and_reference(reference: str) -> tuple[str, str]:
    if "://" in reference:  # Expects format: dmss://DATA_SOURCE/(PATH|ID).Attribute"""
        # The reference points to another data source
        protocol, address = reference.split("://", 1)
        if protocol != Protocols.DMSS.value:
            # Only support one reference type
            raise NotImplementedError(f"The protocol '{protocol}' is not supported")
        data_source_id, reference = address.split("/", 1)
    else:  # Expects format: /DATA_SOURCE/(PATH|ID).Attribute"""
        reference = reference.strip("/. ")  # Remove leading and trailing stuff
        data_source_id, reference = reference.split("/", 1)

    # The data source is given, so rest of reference should start with "/"
    return data_source_id, f"/{reference}"


def resolve_reference_items(
    data_source: DataSource,
    reference_items: list[AttributeItem | QueryItem | IdItem],
    get_data_source: Callable,
    resolve: bool = False,
) -> tuple[list | dict, list[str]]:
    if len(reference_items) == 0 or isinstance(reference_items[0], AttributeItem):
        raise NotFoundException(f"Invalid reference_items {reference_items}.")
    document, id = reference_items[0].get_entry_point(data_source)
    path = [id]
    reference_items.pop(0)
    while len(reference_items):
        if isinstance(reference_items[0], IdItem):
            raise NotFoundException(f"Invalid reference_items {reference_items}.")
        document, attribute = reference_items[0].get_child(
            document, data_source, get_data_source, resolve=len(reference_items) != 1 or resolve
        )
        if isinstance(document, dict) and "_id" in document:
            # Found a new document, use that as new starting point for the attribute path
            path = [document["_id"]]
        else:
            path.append(attribute)
        if not isinstance(document, (list, dict)):
            raise NotFoundException(f"Path {path} leads to a primitive value.")
        reference_items.pop(0)
    return document, path


@dataclass(frozen=True)
class ResolvedReference:
    data_source_id: str
    document_id: str
    attribute_path: list[str]
    entity: dict | list


def resolve_reference(reference: str, get_data_source: Callable, resolve: bool = False) -> ResolvedReference:
    """Resolve the reference into a document.

    resolve: Resolve the target if it's a reference"""
    if not reference:
        raise ApplicationException("Failed to resolve reference. Got empty reference.")

    data_source_id, _reference = split_data_source_and_reference(reference)
    reference_items = reference_to_reference_items(_reference)

    # The first reference item should always be a DataSourceItem
    data_source = get_data_source(data_source_id)
    document, path = resolve_reference_items(data_source, reference_items, get_data_source, resolve=resolve)
    return ResolvedReference(
        entity=document,
        data_source_id=data_source_id,
        document_id=str(path[0]),
        attribute_path=path[1:],
    )
