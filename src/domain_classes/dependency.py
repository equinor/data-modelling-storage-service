from dataclasses import dataclass
from typing import Literal, NewType

TDependencyProtocol = NewType("TDependencyProtocol", Literal["sys", "http"])


@dataclass(frozen=True)
class Dependency:
    """Class for any dependencies (external types) a entity references"""

    alias: str
    # Different ways we support to fetch dependencies.
    # sys: This DMSS instance
    # http: A public HTTP GET call
    protocol: TDependencyProtocol
    address: str
    version: str = ""
