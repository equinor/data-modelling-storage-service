from typing import BinaryIO

from common.tree.tree_node import Node
from enums import SIMOS


def merge_entity_and_files(node: Node, files: dict[str, BinaryIO]):
    """
    Recursively adds the matching posted files to the system/SIMOS/Blob types in the node
    """
    for node_child in node.traverse():  # Traverse the entire Node tree
        if not node_child.entity:  # Skipping empty nodes
            continue
        if node_child.type == SIMOS.BLOB.value:
            try:  # For all Blob Nodes, add the posted file in the Node temporary '_blob_' attribute
                node_child.entity["_blob_"] = files[node_child.entity["name"]]
            except KeyError as ex:
                raise KeyError(
                    "File referenced in entity does not match any ",
                    f"filename posted. Posted files: {tuple(files.keys())}",
                ) from ex
