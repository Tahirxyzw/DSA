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

   

    @staticmethod
    def _is_red(node: Optional["RedBlackTree[T]"]) -> bool:
        return node is not None and node.colour == Colour.Red

    def _rotate_left(self) -> "RedBlackTree[T]":
        x = self.right
        assert x is not None
        self.right = x.left
        x.left = self
        x.colour = self.colour
        self.colour = Colour.Red
        return x

    def _rotate_right(self) -> "RedBlackTree[T]":
        x = self.left
        assert x is not None
        self.left = x.right
        x.right = self
        x.colour = self.colour
        self.colour = Colour.Red
        return x

    def _flip_colours(self) -> None:
        self.colour = Colour.Red if self.colour == Colour.Black else Colour.Black
        if self.left is not None:
            self.left.colour = Colour.Red if self.left.colour == Colour.Black else Colour.Black
        if self.right is not None:
            self.right.colour = Colour.Red if self.right.colour == Colour.Black else Colour.Black

    def _fix_up(self) -> "RedBlackTree[T]":
        if self._is_red(self.right) and not self._is_red(self.left):
            self = self._rotate_left()
        if self._is_red(self.left) and self.left is not None and self._is_red(self.left.left):
            self = self._rotate_right()
        if self._is_red(self.left) and self._is_red(self.right):
            self._flip_colours()
        return self

    def _move_red_left(self) -> "RedBlackTree[T]":
        self._flip_colours()
        if self.right is not None and self._is_red(self.right.left):
            self.right = self.right._rotate_right()
            self = self._rotate_left()
            self._flip_colours()
        return self

    def _move_red_right(self) -> "RedBlackTree[T]":
        self._flip_colours()
        if self.left is not None and self._is_red(self.left.left):
            self = self._rotate_right()
            self._flip_colours()
        return self

    def _min_node(self) -> "RedBlackTree[T]":
        cur = self
        while cur.left is not None:
            cur = cur.left
        return cur

    def _delete_min(self) -> Optional["RedBlackTree[T]"]:
        if self.left is None:
            return None

        if not self._is_red(self.left) and self.left is not None and not self._is_red(self.left.left):
            self = self._move_red_left()

        assert self.left is not None
        self.left = self.left._delete_min()
        return self._fix_up()

    def _insert_rec(self, x: T) -> "RedBlackTree[T]":
        if x < self.value:
            if self.left is None:
                self.left = RedBlackTree(x, Colour.Red)
            else:
                self.left = self.left._insert_rec(x)
        elif x > self.value:
            if self.right is None:
                self.right = RedBlackTree(x, Colour.Red)
            else:
                self.right = self.right._insert_rec(x)
        else:
            raise RuntimeError("Duplicate key insertion is not allowed")

        return self._fix_up()

    def _delete_rec(self, x: T) -> Optional["RedBlackTree[T]"]:
        if x < self.value:
            if self.left is None:
                return self  # not found
            if not self._is_red(self.left) and self.left is not None and not self._is_red(self.left.left):
                self = self._move_red_left()
            assert self.left is not None
            self.left = self.left._delete_rec(x)
        else:
            if self._is_red(self.left):
                self = self._rotate_right()

            if x == self.value and self.right is None:
                return None

            if self.right is None:
                return self  # not found

            if not self._is_red(self.right) and self.right is not None and not self._is_red(self.right.left):
                self = self._move_red_right()

            if x == self.value:
                succ = self.right._min_node()
                self.value = succ.value
                self.right = self.right._delete_min()
            else:
                self.right = self.right._delete_rec(x)

        return self._fix_up()

    

    def is_bst(self) -> bool:
        """Returns true if this tree is a valid binary search tree."""

        def go(node: Optional["RedBlackTree[T]"], lo: Optional[T], hi: Optional[T]) -> bool:
            if node is None:
                return True
            if lo is not None and not (node.value > lo):
                return False
            if hi is not None and not (node.value < hi):
                return False
            return go(node.left, lo, node.value) and go(node.right, node.value, hi)

        return go(self, None, None)

    def is_rbt(self) -> bool:
        """Returns true if this tree is a valid red-black tree."""
        if self.colour != Colour.Black:
            return False
        if not self.is_bst():
            return False

        def no_red_red(node: Optional["RedBlackTree[T]"]) -> bool:
            if node is None:
                return True
            if node.colour == Colour.Red:
                if self._is_red(node.left) or self._is_red(node.right):
                    return False
            return no_red_red(node.left) and no_red_red(node.right)

        def black_height(node: Optional["RedBlackTree[T]"]) -> Optional[int]:
            if node is None:
                return 1  # treating None leaves as black
            lh = black_height(node.left)
            rh = black_height(node.right)
            if lh is None or rh is None or lh != rh:
                return None
            return lh + (1 if node.colour == Colour.Black else 0)

        return no_red_red(self) and (black_height(self) is not None)

    def insert(self, x: T):
        """Inserts a new element into the correct place in this tree."""
        new_root = self._insert_rec(x)

        # mutating in place so external references remain valid
        self.value = new_root.value
        self.colour = new_root.colour
        self.left = new_root.left
        self.right = new_root.right

        self.colour = Colour.Black

    def delete(self, x: T):
        """Deletes an element from this tree, if present."""
        # Skeleton limitation cannot represent empty tree as an instance
        if self.left is None and self.right is None and self.value == x:
            raise RuntimeError("Cannot delete the only node in the tree (skeleton limitation)")

        new_root = self._delete_rec(x)
        if new_root is None:
            #  tree became empty, we already handles the only node case above
            raise RuntimeError("Tree became empty after delete (skeleton limitation)")

        self.value = new_root.value
        self.colour = new_root.colour
        self.left = new_root.left
        self.right = new_root.right

        self.colour = Colour.Black

    def contains(self, x: T) -> bool:
        """Returns true if this tree contains the specified value."""
        cur: Optional["RedBlackTree[T]"] = self
        while cur is not None:
            if x < cur.value:
                cur = cur.left
            elif x > cur.value:
                cur = cur.right
            else:
                return True
        return False



