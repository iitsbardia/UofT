"""CSC148 Prep 9: Binary Search Trees

=== CSC148 Fall 2024 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu and Diane Horton

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 David Liu and Diane Horton

=== Module Description ===
Your task in this prep's synthesize is to implement each of the unimplemented
BinarySearchTree methods in this file.

Take advantage of the BinarySearchTree property to ensure that you are only
making the recursive calls that are required to implement the function:
*** Do NOT make any unnecessary calls! ***
(The prep readings illustrate this idea in the discussion of how __contains__
is implemented.)

NOTE: the doctests access and assign to private attributes directly, which is
not good practice (although python_ta doesn't complain about it in doctests).
"""
from __future__ import annotations
from typing import Any
from python_ta.contracts import check_contracts


@check_contracts
class BinarySearchTree:
    """Binary Search Tree class.

    This class represents a binary tree satisfying the Binary Search Tree
    property: for every node, its value is >= all items stored in its left
    subtree, and <= all items stored in its right subtree.

    Attributes:
    - _root: The item stored at the root of the tree, or None
             if the tree is empty.
    - _left: The left subtree, or None if the tree is empty.
    - _right: The right subtree, or None if the tree is empty.

    Representation Invariants:
    - (self._root is None and self._left is None and self._right is None) or \
        (self._root is not None and isinstance(self._left, BinarySearchTree) \
        and isinstance(self._right, BinarySearchTree))
        # If self._root is None, then so are self._left and self._right.
        # This represents an empty BST.
        # If self._root is not None, then self._left and self._right
        # are BinarySearchTrees. This represents a non-empty BST.
    - (BST Property) If self is not empty, then all items in
      self._left are <= self._root, and all items in
      self._right are >= self._root.
    """
    _root: Any | None
    _left: BinarySearchTree | None
    _right: BinarySearchTree | None

    def __init__(self, root: Any | None) -> None:
        """Initialize a new BST containing only the given root value.

        If <root> is None, initialize an empty tree.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return True if this BST is empty.

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    # -------------------------------------------------------------------------
    # Standard Multiset methods (search)
    # -------------------------------------------------------------------------
    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this BST.

        >>> bst = BinarySearchTree(3)
        >>> bst._left = BinarySearchTree(2)
        >>> bst._right = BinarySearchTree(5)
        >>> 3 in bst
        True
        >>> 5 in bst
        True
        >>> 2 in bst
        True
        >>> 4 in bst
        False
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item < self._root:
            return item in self._left  # or, self._left.__contains__(item)
        else:
            return item in self._right  # or, self._right.__contains__(item)

    # -------------------------------------------------------------------------
    # Additional BST methods
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        """Return a string representation of this BST.

        This string uses indentation to show depth.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this BST.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            answer = depth * '  ' + str(self._root) + '\n'
            answer += self._left._str_indented(depth + 1)
            answer += self._right._str_indented(depth + 1)
            return answer

    # -------------------------------------------------------------------------
    # Prep exercises
    # -------------------------------------------------------------------------
    def maximum(self) -> int | None:
        """Return the maximum number in this BST, or None if this BST is empty.

        Hint: Review the BST property to ensure you aren't making unnecessary
        recursive calls.

        >>> BinarySearchTree(None).maximum() is None   # Empty BST
        True
        >>> BinarySearchTree(10).maximum()
        10
        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(3)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.maximum()
        13
        """
        if self.is_empty():
            return None

        current = self
        while current._right is not None and not current._right.is_empty():
            current = current._right

        return current._root

    def count(self, item: Any) -> int:
        """Return the number of occurrences of <item> in this BST.

        Hint: carefully review the BST property!

        >>> BinarySearchTree(None).count(148)  # An empty BST
        0
        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(3)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.count(7)
        1
        >>> bst.count(3)
        2
        >>> bst.count(100)
        0
        """
        if self.is_empty():
            return 0
        count = 0
        if self._root == item:
            count += 1
            left_count = self._left.count(item) if self._left else 0
            right_count = self._right.count(item) if self._right else 0
            return count + left_count + right_count
        elif item < self._root:
            return count + self._left.count(item) if self._left else count
        else:
            return count + self._right.count(item) if self._right else count

    def items(self) -> list:
        """Return all of the items in the BST in sorted order.

        You should *not* need to sort the list yourself: instead, use the BST
        property and combine self._left.items() and self._right.items()
        in the correct order!

        >>> BinarySearchTree(None).items()  # An empty BST
        []
        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.items()
        [2, 3, 5, 7, 9, 11, 13]
        """
        if self.is_empty():
            return []

        left_items = []
        if self._left:
            left_items = self._left.items()
        right_items = []
        if self._right:
            right_items = self._right.items()

        return left_items + [self._root] + right_items

    def smaller(self, item: Any) -> list:
        """Return all of the items in this BST strictly smaller than <item>.

        The items are returned in sorted order.

        Precondition: all items in this BST can be compared with <item>.

        As with BinarySearchTree.items, you should *not* need to sort the list
        yourself!

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.smaller(6)
        [2, 3, 5]
        >>> bst.smaller(13)
        [2, 3, 5, 7, 9, 11]
        """
        if self.is_empty():
            return []

        result = []

        if self._left:
            result.extend(self._left.smaller(item))

        if self._root < item:
            result.append(self._root)

            if self._right:
                result.extend(self._right.smaller(item))

        return result


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # import python_ta
    #
    # python_ta.check_all(config={'max-line-length': 100})
