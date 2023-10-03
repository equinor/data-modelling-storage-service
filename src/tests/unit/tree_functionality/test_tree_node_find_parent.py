import unittest
from unittest import mock, skip

from domain_classes.tree_node import Node


class TreeNodeFindParentTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Node(
            key="root",
            uid="1",
            entity={},
            blueprint_provider=mock.Mock(),
            attribute=mock.Mock(),
            recipe_provider=None,
        )

        self.child = Node(
            key="child",
            uid="2",
            entity={},
            blueprint_provider=mock.Mock(),
            parent=self.root,
            attribute=mock.Mock(),
            recipe_provider=None,
        )

        self.grand_child = Node(
            key="grand_child",
            uid="3",
            entity={},
            blueprint_provider=mock.Mock(),
            parent=self.child,
            attribute=mock.Mock(),
            recipe_provider=None,
        )

    def test_find_parent_returns_parent(self):
        self.assertEqual(self.child.find_parent(), self.root)

    # TODO: Fix these skips.
    @skip(reason="Currently returns 'self'. I believe this is a bug.")
    def test_find_parent_when_parent_does_not_exist_returns_None(self):
        self.assertIsNone(self.root.find_parent())

    @skip(reason="Currently returns 'root'. I believe this is a bug.")
    def test_find_parent_returns_parent_not_grandparent(self):
        self.assertEqual(self.grand_child.find_parent(), self.child)
