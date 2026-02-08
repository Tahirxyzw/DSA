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
    
   
    def contains(self, x: T) -> bool:
        """Returns true if this tree contains the specified value."""
        #checking if its the value we are looking for, if not we check if its less than the value and go left otherwise we go right
        if x == self.value:
            return True
        elif x < self.value:
            return self.left.contains(x) if self.left else False
        else:
            return self.right.contains(x) if self.right else False
    
   
    def is_bst(self) -> bool:
        """Returns true if this tree is a valid binary search tree."""
        return self._is_bst_helper(None, None)
    
    def _is_bst_helper(self, min_val, max_val) -> bool:
        if min_val is not None and self.value <= min_val:
            return False
        if max_val is not None and self.value >= max_val:
            return False
        
        left_ok = (
            self.left._is_bst_helper(min_val, self.value)
            if self.left else True
        )
        right_ok = (
            self.right._is_bst_helper(self.value, max_val)
            if self.right else True
        )
        return left_ok and right_ok
    
   
    def is_rbt(self) -> bool:
        """Returns true if this tree is a valid red-black tree."""
        # Root of RBT must be black
        if self.colour != Colour.Black:
            return False
        # Must be a valid BST
        if not self.is_bst():
            return False
        # No red-red violations and consistent black height
        return self._no_red_red() and self._black_height() != -1
    
    def _no_red_red(self) -> bool:
        #Checking that no red node has a red child
        if self.colour == Colour.Red:
            if (self.left and self.left.colour == Colour.Red) or \
               (self.right and self.right.colour == Colour.Red):
                return False
        
        left_ok = self.left._no_red_red() if self.left else True
        right_ok = self.right._no_red_red() if self.right else True
        return left_ok and right_ok
    
    def _black_height(self) -> int:
        #Returning black height, or -1 if inconsistent
        left_h = self.left._black_height() if self.left else 0
        right_h = self.right._black_height() if self.right else 0
        
        if left_h == -1 or right_h == -1 or left_h != right_h:
            return -1
        
        return left_h + (1 if self.colour == Colour.Black else 0)
    
  
    def _is_red(self, node):
        #Checking if a node is red 
        return node is not None and node.colour == Colour.Red
    
    def _rotate_left(self):
        #Performing the left rotation
        x = self.right
        self.right = x.left
        x.left = self
        x.colour = self.colour
        self.colour = Colour.Red
        return x
    
    def _rotate_right(self):
        #Performing the right rotation
        x = self.left
        self.left = x.right
        x.right = self
        x.colour = self.colour
        self.colour = Colour.Red
        return x
    
    def _flip_colours(self):
        #Flipping colours during balancing
        self.colour = Colour.Red
        if self.left:
            self.left.colour = Colour.Black
        if self.right:
            self.right.colour = Colour.Black
    

    def insert(self, x: T):
        #Inserting a new element into the correct place in the tree
        root = self._insert(x)
        root.colour = Colour.Black
        return root
    
    def _insert(self, x: T):
        #Helper for insertion with LLRB balancing
        # BST insert
        if x < self.value:
            if self.left:
                self.left = self.left._insert(x)
            else:
                self.left = RedBlackTree(x, Colour.Red)
        elif x > self.value:
            if self.right:
                self.right = self.right._insert(x)
            else:
                self.right = RedBlackTree(x, Colour.Red)
        # not inserting duplicates
        
        # Applying LLRB fix up rules
        return self._fix_up()
    
    def _fix_up(self) -> "RedBlackTree[T]":
        #Fix up after insertion to maintain LLRB properties
        # If right child is red and left is black rotating left
        if self._is_red(self.right) and not self._is_red(self.left):
            self = self._rotate_left()
        
        # If left child is red and its left child is red rotating right
        if self._is_red(self.left) and self._is_red(self.left.left):
            self = self._rotate_right()
        
        # If both children are red flipping colors
        if self._is_red(self.left) and self._is_red(self.right):
            self._flip_colours()
        
        return self
    
  
    def delete(self, x: T):
        """Deletes an element from this tree, if present."""
        if x < self.value and self.left:
            self.left = self.left.delete(x)
        elif x > self.value and self.right:
            self.right = self.right.delete(x)
        elif x == self.value:
            # No left child
            if not self.left:
                return self.right
            # No right child
            if not self.right:
                return self.left
            # Two children - replacing it with the successor
            successor = self.right._min()
            self.value = successor.value
            self.right = self.right.delete(successor.value)
        return self
    
    def _min(self):
        # Finding the minimum value node in subtree
        return self if not self.left else self.left._min()