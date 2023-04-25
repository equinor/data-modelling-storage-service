import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, Tuple, Union

from common.exceptions import ApplicationException, NotFoundException
from common.utils.data_structure.find import find
from common.utils.data_structure.is_same import is_same
from common.utils.is_reference import is_reference
from enums import Protocols
from storage.data_source_class import DataSource


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


def reference_to_reference_items(reference: str, items=None, prev_deliminator=None):
    """Split up the reference into reference items."""

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

    if "$" in content:  # By id
        items.append(IdItem(content[1:]))
    elif prev_deliminator == "/":
        if len(items) > 0:  # By package
            items.append(AttributeItem("content"))
            items.append(QueryItem(query=f"name={content}"))
        else:  # By root package
            items.append(QueryItem(query=f"name={content},isRoot=True"))
    elif prev_deliminator == "(" and deliminator == ")":  # By query
        items.append(QueryItem(query=content))
    elif prev_deliminator == "[" and deliminator == "]":  # By list index
        items.append(AttributeItem(f"[{content}]"))
    elif prev_deliminator == ".":  # By attribute
        items.append(AttributeItem(content))
    else:  # Fallback to support the old reference format
        items.append(IdItem(content))

    return reference_to_reference_items(remaining_reference, items, deliminator)


@dataclass
class IdItem:
    """Points to an id."""

    id: str

    def resolve(self, document: dict | list, data_source: DataSource, get_data_source: Callable) -> dict:
        # Get the document from the data source
        return data_source.get(self.id)


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

    def resolve(self, document: dict | list, data_source: DataSource, get_data_source: Callable) -> dict | None:
        # We need to search inside the data source for the document
        if not document:
            result: list[dict] = data_source.find(self.filter())
            if not result:
                raise NotFoundException(
                    f"No document that match '{self.query}', in data source '{data_source.name}' could be found."
                )
            if len(result) > 2:
                raise ApplicationException(
                    f"More than 1 document that match '{self.query}' was returned from DataSource. That should not happen..."
                )
            return result[0]

        # Search inside an existing document (need to resolve any references first before trying to compare against filter)
        elements = [
            resolve_reference(f["address"], data_source, get_data_source) if is_reference(f) else f for f in document
        ]  # Resolve any references
        return next(
            (f for f in elements if is_same(f, self.filter())), None
        )  # Find an item that match the given filter


@dataclass
class AttributeItem:
    """Move into a key of an object or find an item in a list based on index position."""

    path: str

    def resolve(self, document: dict | list, data_source: DataSource, get_data_source: Callable) -> dict:
        try:
            result = find(document, [self.path])
        except (IndexError, TypeError, KeyError):
            raise NotFoundException(f"No '{self.path}' inside the '{str(document)}' exist.")

        if is_reference(result):
            return resolve_reference(result["address"], data_source, get_data_source)
        return result


def resolve_reference_items(
    data_source: DataSource,
    reference_items: list[AttributeItem | QueryItem | IdItem],
    get_data_source: Callable,
    document=None,
):
    if len(reference_items) == 0:
        return document
    resolved_document = reference_items[0].resolve(document, data_source, get_data_source)
    return resolve_reference_items(data_source, reference_items[1:], get_data_source, resolved_document)


def resolve_reference(reference: str, data_source: DataSource, get_data_source: Callable) -> dict:
    """Resolve the reference into a document."""

    if "://" in reference:
        # The reference points to another data source
        protocol, address = reference.split("://", 1)
        if protocol != Protocols.DMSS.value:
            # Only support one reference type
            raise NotImplementedError(f"The protocol '{protocol}' is not supported")
        data_source_id, reference = address.split("/", 1)
        data_source = get_data_source(data_source_id)
        reference = f"/{reference}"  # The data source is given, so should start with an /

    reference_items = reference_to_reference_items(reference)
    document = resolve_reference_items(data_source, reference_items, get_data_source)
    if not document:
        raise NotFoundException(
            f"No document found that matches '{reference}', in the data source '{data_source.name}' could be found."
        )
    return document
