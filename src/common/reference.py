from common.exceptions import ApplicationException
from enums import Protocols


class Reference:
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
    def fromabsolute(cls, reference: str):
        """Returns an instance of the Reference class based on the reference input

        @param reference: Must be on one of the following formats
            - dmss://DATA_SOURCE/(PATH|ID).Attribute
            - DATA_SOURCE/(PATH|ID).Attribute
            - /DATA_SOURCE/(PATH|ID).Attribute
        """
        protocol = Protocols.DMSS.value
        path = None
        reference = reference.strip("/. ")
        if "://" in reference:
            protocol, reference = reference.split("://", 1)
        if "/" in reference:
            reference, path = reference.split("/", 1)
        return cls(path, reference, protocol)

    @classmethod
    def fromrelative(cls, reference: str, document_id: str | None, data_source: str):
        if "://" in reference:
            # Already contains protocol and data source
            return cls.fromabsolute(reference)
        elif reference.startswith("^"):
            if not document_id:
                raise ApplicationException(
                    "Document id is missing and therefore it is not possible to replace ^ with an id reference."
                )
            return cls(reference.replace("^", f"${document_id}"), data_source)
        else:
            return cls(reference, data_source)
