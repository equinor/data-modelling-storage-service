"""Storing a list of documents costs a fixed number of round trips, not a number per document.

The number to watch is requests, not operations: a bulk write of N documents still updates N
documents, so operation counts look the same either way. These tests therefore count calls that
leave the process rather than documents stored, and check that taking the batched path leaves a
document indistinguishable from one written singly.

Writing a document on its own costs four such calls: read its lookup, write its lookup, write the
document, cache the document. The batched path reads every lookup at once, writes the new ones at
once, writes the documents once per repository, and caches them at once, so the cost stops
growing with the size of the batch.

The last three cover what a bulk write does to the document cache. It writes the documents it
stored, which is one round trip rather than one per document, and which leaves no document being
served with the body it had before it was overwritten.
"""

import pytest

from authentication.models import AccessControlList, AccessLevel, User
from common.exceptions import BadRequestException
from storage.data_source_class import DataSource
from storage.repository_interface import RepositoryInterface


class _FakeRepository:
    def __init__(self):
        self.name = "repo"
        self.data_types = []
        self.documents: dict[str, dict] = {}
        self.update_calls = 0
        self.bulk_update_calls = 0

    def update(self, uid: str, document: dict) -> bool:
        self.update_calls += 1
        self.documents[uid] = document
        return True

    def get(self, uid: str) -> dict | None:
        return self.documents.get(uid)

    def bulk_update(self, documents: list[dict]) -> bool:
        self.bulk_update_calls += 1
        self.documents.update({document["_id"]: document for document in documents})
        return True


class _FakeKeyValueStore:
    def __init__(self):
        self.values: dict[str, dict] = {}
        self.round_trips: list[str] = []

    def get(self, key: str):
        self.round_trips.append("get")
        return self.values.get(key)

    def get_many(self, keys: list[str]) -> list[dict | None]:
        if not keys:
            return []
        self.round_trips.append("get_many")
        return [self.values.get(key) for key in keys]

    def set(self, key: str, value: dict, ttl: int | None = None) -> None:
        self.round_trips.append("set")
        self.values[key] = value

    def set_many(self, values: dict[str, dict], ttl: int | None = None) -> None:
        if not values:
            return
        self.round_trips.append("set_many")
        self.values.update(values)

    def delete(self, key: str) -> None:
        self.round_trips.append("delete")
        self.values.pop(key, None)


def _data_source() -> tuple[DataSource, _FakeRepository, _FakeKeyValueStore]:
    repository = _FakeRepository()
    lookups = _FakeKeyValueStore()
    data_source = DataSource(
        name="testing",
        user=User(user_id="owner", scope=AccessLevel.WRITE),
        acl=AccessControlList.default(),
        repositories={"repo": repository},
        acl_lookup_db=lookups,
        document_cache=_FakeKeyValueStore(),
    )
    return data_source, repository, lookups


def _round_trips(data_source: DataSource, repository: _FakeRepository, lookups: _FakeKeyValueStore) -> int:
    """Every call that would leave the process: to Redis for lookups, to Redis for the cache, to Mongo."""
    return (
        len(lookups.round_trips)
        + len(data_source.document_cache.round_trips)
        + repository.update_calls
        + repository.bulk_update_calls
    )


def test_many_documents_are_written_in_one_round_trip():
    data_source, repository, _ = _data_source()

    data_source.update_many([{"_id": str(number), "type": "Test"} for number in range(50)])

    assert repository.bulk_update_calls == 1, "one round trip should carry every document"
    assert repository.update_calls == 0, "no document should be written on its own"
    assert len(repository.documents) == 50


def test_an_empty_list_does_not_touch_the_repository():
    data_source, repository, _ = _data_source()

    data_source.update_many([])

    assert repository.bulk_update_calls == 0
    assert repository.update_calls == 0


def test_a_bulk_write_costs_the_same_whether_it_carries_ten_documents_or_a_thousand():
    small_source, small_repository, small_lookups = _data_source()
    large_source, large_repository, large_lookups = _data_source()

    small_source.update_many([{"_id": str(number), "type": "Test"} for number in range(10)])
    large_source.update_many([{"_id": str(number), "type": "Test"} for number in range(1000)])

    small = _round_trips(small_source, small_repository, small_lookups)
    large = _round_trips(large_source, large_repository, large_lookups)
    assert small == large, f"a hundredfold larger batch cost {large} round trips rather than {small}"
    assert large == 4, "read the lookups, write the new lookups, write the documents, empty the cache"


def test_a_bulk_write_costs_far_less_than_writing_each_document_on_its_own():
    batched_source, batched_repository, batched_lookups = _data_source()
    singly_source, singly_repository, singly_lookups = _data_source()

    batched_source.update_many([{"_id": str(number), "type": "Test"} for number in range(80)])
    for number in range(80):
        singly_source.update({"_id": str(number), "type": "Test"})

    singly = _round_trips(singly_source, singly_repository, singly_lookups)
    batched = _round_trips(batched_source, batched_repository, batched_lookups)
    assert singly == 4 * 80, "writing a document on its own reads and writes its lookup, stores it, and caches it"
    assert batched * 20 < singly, f"batching eighty documents saved only {singly - batched} round trips"


def test_the_lookups_of_a_batch_are_read_and_written_together():
    data_source, _, lookups = _data_source()

    data_source.update_many([{"_id": str(number), "type": "Test"} for number in range(50)])

    assert lookups.round_trips == ["get_many", "set_many"], "fifty lookups, one read and one write"
    assert len(lookups.values) == 50, "every document must still end up with a lookup of its own"


def test_a_batch_reads_the_acl_it_inherits_once_not_once_per_document():
    data_source, _, lookups = _data_source()
    data_source.update({"_id": "parent", "type": "Test"})
    lookups.round_trips.clear()

    data_source.update_many([{"_id": str(number), "type": "Test"} for number in range(50)], parent_id="parent")

    assert lookups.round_trips.count("get") == 1, "the parent is the same for every document in the batch"


def test_documents_that_already_exist_do_not_have_their_lookups_written_again():
    data_source, _, lookups = _data_source()
    data_source.update_many([{"_id": str(number), "type": "Test"} for number in range(20)])
    lookups.round_trips.clear()

    data_source.update_many([{"_id": str(number), "type": "Test", "description": "again"} for number in range(20)])

    assert lookups.round_trips == ["get_many"], "the lookups were all found, so there was nothing to write"


def test_a_batched_document_is_stored_like_a_single_one():
    data_source, repository, lookups = _data_source()

    data_source.update({"_id": "1", "type": "Test", "name": "singly"})
    data_source.update_many([{"_id": "2", "type": "Test", "name": "batched"}])

    singly, batched = lookups.values["testing:1"], lookups.values["testing:2"]
    assert batched["repository"] == singly["repository"]
    assert batched["acl"] == singly["acl"], "a batched write must inherit access control the same way"
    assert repository.documents["2"]["name"] == "batched"


def test_an_id_is_generated_for_a_batched_document_that_has_none():
    data_source, repository, _ = _data_source()
    document = {"type": "Test"}

    data_source.update_many([document])

    assert document["_id"], "the caller needs the generated id back, as it does from update"
    assert list(repository.documents) == [document["_id"]]


def test_a_batch_with_an_invalid_document_name_stores_nothing():
    data_source, repository, _ = _data_source()

    with pytest.raises(BadRequestException, match="invalid document name"):
        data_source.update_many(
            [
                {"_id": "1", "type": "Test", "name": "valid_name"},
                {"_id": "2", "type": "Test", "name": "not a valid name"},
            ]
        )

    assert repository.documents == {}, "the batch is rejected before any of it reaches the repository"


def test_a_repository_that_cannot_batch_still_stores_every_document():
    """Only Mongo can batch. Every other backend inherits the fallback on RepositoryInterface."""

    class _UnbatchedRepository:
        bulk_update = RepositoryInterface.bulk_update

        def __init__(self):
            self.documents: dict[str, dict] = {}

        def update(self, uid: str, document: dict, **kwargs) -> bool:
            self.documents[uid] = document
            return True

    repository = _UnbatchedRepository()

    assert repository.bulk_update([{"_id": "1"}, {"_id": "2"}]) is True
    assert repository.documents.keys() == {"1", "2"}


def test_a_bulk_write_caches_its_documents_in_one_round_trip():
    data_source, repository, _ = _data_source()

    data_source.update_many([{"_id": str(number), "type": "Test"} for number in range(50)])

    assert len(repository.documents) == 50, "the documents must still reach the repository"
    assert len(data_source.document_cache.values) == 50, "a bulk write must cache what it stored"
    assert data_source.document_cache.round_trips == ["set_many"], "fifty documents, cached in one call"


def test_a_bulk_write_replaces_the_documents_it_overwrites_in_the_cache():
    data_source, _, _ = _data_source()
    data_source.update_many([{"_id": "1", "type": "Test", "description": "first"}])
    # Read it back so the cache holds the old body, the way any reader between the two writes would.
    assert data_source.get("1")["description"] == "first"
    assert data_source.document_cache.values["testing:1"]["description"] == "first"

    data_source.update_many([{"_id": "1", "type": "Test", "description": "second"}])

    assert data_source.document_cache.values["testing:1"]["description"] == "second", "no stale body may survive"
    assert data_source.get("1")["description"] == "second", "the stale document must not be served"


def test_a_read_after_a_bulk_write_does_not_go_to_the_repository():
    data_source, repository, _ = _data_source()
    data_source.update_many([{"_id": "1", "type": "Test"}, {"_id": "2", "type": "Test"}])
    repository.documents.clear()  # Only a cache hit can answer the read now.

    assert data_source.get("1") == {"_id": "1", "type": "Test"}
    assert data_source.get("2") == {"_id": "2", "type": "Test"}
