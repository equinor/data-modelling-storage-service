import re

from common.exceptions import ApplicationException
from enums import Protocols


class Address:
    def __repr__(self):
        path = f"/{self.path}" if self.path else ""
        return f"{self.protocol}://{self.data_source}{path}"

    def __init__(self, path: str | None, data_source: str, protocol: str = Protocols.DMSS.value):
        if protocol and protocol != Protocols.DMSS.value:
            # Only support one reference type
            raise NotImplementedError(f"The protocol '{protocol}' is not supported")
        self.protocol = protocol
        self.data_source = data_source
        self.path = path

    @classmethod
    def from_absolute(cls, address: str):
        """Returns an instance of the Address class based on the address input

        @param address: Must be on one of the following formats (.Attribute is optional)
            - dmss://DATA_SOURCE/(PATH|$ID).Attribute
            - DATA_SOURCE/(PATH|$ID).Attribute
            - /DATA_SOURCE/(PATH|$ID).Attribute
        """
        protocol = Protocols.DMSS.value
        path = None
        address = address.strip("/. ")
        if "://" in address:
            protocol, address = address.split("://", 1)
        if "/" in address:
            address, path = address.split("/", 1)
        return cls(path, address, protocol)

    @classmethod
    def from_relative(cls, address: str, document_id: str | None, data_source: str):
        if "://" in address:
            # Already contains protocol and data source
            return cls.from_absolute(address)
        elif address.startswith("^"):
            if not document_id:
                raise ApplicationException(
                    "Document id is missing and therefore it is not possible to replace ^ with an id reference."
                )
            return cls(address.replace("^", f"${document_id}"), data_source)
        else:
            return cls(address, data_source)

    def is_by_package(self) -> bool:
        if not self.path:
            return False
        # This checks if the path is by package path format,
        # then the last part of that part points directly to an entity.
        return len(re.findall("/([A-Za-z0-9_-]*)$", self.path)) > 0
