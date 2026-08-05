"""A bulk write survives the faults that pass on their own, and gives up on the ones that do not.

The client is built with 'retryWrites=False', so the driver retries nothing for us. That leaves
'bulk_update' as the only thing standing between a transient fault and a lost batch, and network
faults are the ones most likely to be transient: a dropped connection, a timed-out socket, a
primary that has not finished being elected.

Those faults do not reach the server as a failed write, so they are not 'OperationFailure' and were
not retried. The tests below pin both halves of the boundary, since widening a caught exception is
only correct if it stops where it should: a fault that will not pass on its own must still be
raised rather than slept over fifty times.
"""

import traceback
from unittest import mock

import pytest
from pymongo.errors import (
    AutoReconnect,
    BulkWriteError,
    ConnectionFailure,
    InvalidOperation,
    NetworkTimeout,
    ServerSelectionTimeoutError,
)

from storage.repositories.mongo import MongoDBClient


def _client(side_effect):
    """A MongoDBClient whose 'bulk_write' behaves as given, built without opening a connection."""
    client = MongoDBClient.__new__(MongoDBClient)
    client.collection = "collection"
    collection = mock.MagicMock()
    collection.bulk_write.side_effect = side_effect
    client.handler = {"collection": collection}
    return client, collection


def _fails_n_times_with(error, count):
    attempts = {"n": 0}

    def bulk_write(operations, ordered):
        attempts["n"] += 1
        if attempts["n"] <= count:
            raise error
        return mock.MagicMock(acknowledged=True)

    return bulk_write


@pytest.mark.parametrize(
    "error",
    [
        AutoReconnect("connection lost"),
        NetworkTimeout("socket timed out"),
        ServerSelectionTimeoutError("no primary available"),
        ConnectionFailure("connection refused"),
    ],
    ids=["auto_reconnect", "network_timeout", "no_server_selected", "connection_refused"],
)
def test_a_batch_interrupted_by_a_network_fault_is_sent_again(error):
    client, collection = _client(_fails_n_times_with(error, 2))

    with mock.patch("storage.repositories.mongo.sleep"):
        assert client.bulk_update([{"_id": "a"}, {"_id": "b"}]) is True

    assert collection.bulk_write.call_count == 3


def test_a_batch_that_never_reconnects_is_raised_rather_than_retried_forever():
    client, collection = _client(AutoReconnect("connection lost"))

    with mock.patch("storage.repositories.mongo.sleep"), pytest.raises(AutoReconnect):
        client.bulk_update([{"_id": "a"}])

    assert collection.bulk_write.call_count == 6


def test_a_batch_that_is_giving_up_is_not_slept_on_first():
    """The backoff after the last attempt bought no further attempt, so it is no longer waited."""
    client, collection = _client(AutoReconnect("connection lost"))

    with mock.patch("storage.repositories.mongo.sleep") as slept, pytest.raises(AutoReconnect):
        client.bulk_update([{"_id": "a"}])

    assert collection.bulk_write.call_count == 6
    assert slept.call_count == 5


def test_the_backoff_between_attempts_grows_but_is_capped():
    client, _ = _client(AutoReconnect("connection lost"))

    with mock.patch("storage.repositories.mongo.sleep") as slept, pytest.raises(AutoReconnect):
        client.bulk_update([{"_id": "a"}])

    assert [call.args[0] for call in slept.call_args_list] == [2, 4, 8, 16, 30]


def test_the_fault_that_is_raised_is_the_one_the_driver_met():
    """Re-raising bare keeps the traceback on the driver call rather than on the retry loop.

    'raise ex' would preserve the original traceback too, but would add a frame pointing at the
    're-raise' itself, burying the call that actually failed one frame deeper for every attempt.
    """
    error = AutoReconnect("connection lost")
    client, _ = _client(error)

    with mock.patch("storage.repositories.mongo.sleep"), pytest.raises(AutoReconnect) as raised:
        client.bulk_update([{"_id": "a"}])

    assert raised.value is error
    frames = traceback.extract_tb(raised.value.__traceback__)
    ours = [frame for frame in frames if frame.name == "bulk_update"]
    assert ours, "the traceback should still pass through bulk_update"
    assert all("bulk_write" in (frame.line or "") for frame in ours)
    assert not any((frame.line or "").startswith("raise") for frame in ours)


def test_a_partially_applied_batch_is_sent_again():
    """'BulkWriteError' is an 'OperationFailure', so this held before and must keep holding."""
    error = BulkWriteError({"writeErrors": [{"index": 0, "code": 16500, "errmsg": "rate limited"}]})
    client, collection = _client(_fails_n_times_with(error, 2))

    with mock.patch("storage.repositories.mongo.sleep"):
        assert client.bulk_update([{"_id": "a"}, {"_id": "b"}]) is True

    assert collection.bulk_write.call_count == 3


def test_a_fault_that_will_not_pass_on_its_own_is_raised_at_once():
    client, collection = _client(InvalidOperation("cannot do an empty bulk write"))

    with mock.patch("storage.repositories.mongo.sleep"), pytest.raises(InvalidOperation):
        client.bulk_update([{"_id": "a"}])

    assert collection.bulk_write.call_count == 1


def test_a_retried_batch_is_sent_whole_every_time():
    """Every operation is an upsert by '_id', so re-sending a batch that half applied is safe."""
    client, collection = _client(_fails_n_times_with(AutoReconnect("connection lost"), 1))

    with mock.patch("storage.repositories.mongo.sleep"):
        client.bulk_update([{"_id": "a"}, {"_id": "b"}, {"_id": "c"}])

    sent = [call.args[0] for call in collection.bulk_write.call_args_list]
    assert [len(operations) for operations in sent] == [3, 3]
    assert all(operation._upsert for operation in sent[-1])


def test_an_empty_batch_never_reaches_the_database():
    client, collection = _client(AssertionError("should not be called"))

    assert client.bulk_update([]) is True
    assert collection.bulk_write.call_count == 0
