from enum import Enum
from typing import Optional, TypeVar

T = TypeVar("T")
"""Type variable used for the type of value stored in a tree."""


class Colour(Enum):
    """The colour of a node in a red-black tree."""

    Red = 0
    Black = 1


class RedBlackTree[T]:
    """A red-black tree."""

    value: T
    colour: Colour
    left: Optional["RedBlackTree[T]"]
    right: Optional["RedBlackTree[T]"]

    def __init__(self, value, colour, left=None, right=None):
        self.value = value
        self.colour = colour
        self.left = left
        self.right = right

    @staticmethod
    def fromList(xs: list[T]) -> Optional["RedBlackTree[T]"]:
        """Constructs a red-black tree from a list of values.

        Returns None if the list was empty.
        """
        if len(xs) == 0:
            return None

        tree = RedBlackTree(xs[0], Colour.Black)
        for x in xs[1:]:
            tree.insert(x)
        return tree

    def is_bst(self) -> bool:
        """Returns true if this tree is a valid binary search tree."""
        raise NotImplementedError()

    def is_rbt(self) -> bool:
        """Returns true if this tree is a valid red-black tree."""
        raise NotImplementedError()

    def insert(self, x: T):
        """Inserts a new element into the correct place in this tree."""
        raise NotImplementedError()

    def delete(self, x: T):
        """Deletes an element from this tree, if present."""
        raise NotImplementedError()

    def contains(self, x: T) -> bool:
        """Returns true if this tree contains the specified value."""
        raise NotImplementedError()
