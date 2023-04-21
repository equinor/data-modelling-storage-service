from typing import Literal, NewType

from pydantic import BaseModel

TDependencyProtocol = NewType("TDependencyProtocol", Literal["dmss", "http"])  # type: ignore


class Dependency(BaseModel):
    """Class for any dependencies (external types) a entity references"""

    alias: str
    type: str
    # Different ways we support to fetch dependencies.
    # sys: This DMSS instance
    # http: A public HTTP GET call
    protocol: TDependencyProtocol
    address: str
    version: str = ""

    def get_prefix(self):
        return f"{self.protocol}://{self.address}/"
