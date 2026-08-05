"""The abstract data source declares the same calls the concrete one answers.

Nothing subclasses the abstract 'DataSource'; the concrete one does not inherit it. That removes
the check Python would otherwise do for us, so a signature can drift on one side and be noticed by
nobody until a caller written against the interface meets the implementation.

The drift is not harmless in either direction. A parameter the abstract omits cannot be passed by a
caller that holds the interface, even though the implementation accepts it, and the type checker
rejects the call. A parameter the abstract omits that the implementation *requires* is worse: the
call type-checks and then fails at run time.

So the signatures are compared here, which is the check the missing inheritance would have done.
"""

import inspect

import pytest

from storage.data_source_class import DataSource as ConcreteDataSource
from storage.data_source_interface import DataSource as AbstractDataSource

ABSTRACT_METHOD_NAMES = sorted(AbstractDataSource.__abstractmethods__)


def test_the_abstract_data_source_declares_something_to_compare():
    assert ABSTRACT_METHOD_NAMES


@pytest.mark.parametrize("name", ABSTRACT_METHOD_NAMES)
def test_the_concrete_data_source_answers_the_call_the_abstract_one_declares(name):
    declared = getattr(AbstractDataSource, name)
    implemented = getattr(ConcreteDataSource, name, None)

    assert implemented is not None, f"'{name}' is declared abstract but the concrete data source has no such call"
    assert str(inspect.signature(declared)) == str(inspect.signature(implemented)), (
        f"'{name}' is declared as '{inspect.signature(declared)}' "
        f"but implemented as '{inspect.signature(implemented)}'"
    )


def test_a_batch_can_be_written_into_a_parent_through_the_interface():
    """The two arguments that place a batch under its parent are part of the declared call."""
    parameters = inspect.signature(AbstractDataSource.update_many).parameters

    assert "storage_attribute" in parameters
    assert "parent_id" in parameters
    assert parameters["storage_attribute"].default is None
    assert parameters["parent_id"].default is None


def test_a_data_source_is_declared_to_be_built_with_the_blueprints_it_reads():
    """'get_blueprint' has no default, so a caller left to guess it from the interface would fail."""
    parameters = inspect.signature(AbstractDataSource.from_dict).parameters

    assert "get_blueprint" in parameters
    assert parameters["get_blueprint"].default is inspect.Parameter.empty
