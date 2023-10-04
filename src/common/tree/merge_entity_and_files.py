from typing import BinaryIO, Dict

from common.tree.tree_node import Node
from enums import SIMOS


def merge_entity_and_files(node: Node, files: Dict[str, BinaryIO]):
    """
    Recursively adds the matching posted files to the system/SIMOS/Blob types in the node
    """
    for node in node.traverse():  # Traverse the entire Node tree
        if not node.entity:  # Skipping empty nodes
            continue
        if node.type == SIMOS.BLOB.value:
            try:  # For all Blob Nodes, add the posted file in the Node temporary '_blob_' attribute
                node.entity["_blob_"] = files[node.entity["name"]]
            except KeyError:
                raise KeyError(
                    "File referenced in entity does not match any ",
                    f"filename posted. Posted files: {tuple(files.keys())}",
                )
