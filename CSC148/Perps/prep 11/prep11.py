"""CSC148 Prep 11: Review

=== CSC148 Fall 2024 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Sophia Huynh

=== Module Description ===
Your task in this prep's synthesize is to implement the unimplemented
BinarySearchTree and Tree methods in this file.

Take advantage of the BinarySearchTree property to ensure that you are only
making the recursive calls that are required to implement the function:
*** Do NOT make any unnecessary calls! ***

NOTE: the doctests access and assign to private attributes directly, which is
not good practice (although python_ta doesn't complain about it in doctests).
"""
from __future__ import annotations
from typing import Any


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

    def __len__(self) -> int:
        """Return the number of nodes in this BST.

        >>> bst = BinarySearchTree(3)
        >>> bst._left = BinarySearchTree(2)
        >>> bst._right = BinarySearchTree(5)
        >>> len(bst)
        3
        """
        if self.is_empty():
            return 0
        else:
            return len(self._left) + len(self._right) + 1

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
    def kth_smallest(self, k: int) -> Any | None:
        """Return the kth smallest element in this BST or
        None if this BST does not have at least k elements.

        You should NOT use items() and should only use __len__ and recursive
        calls to kth_smallest.

        Hint: Review the BST property to ensure you aren't making unnecessary
        recursive calls.

        Hint 2: You may want to look at prep10's kth_smallest for intuition.

        >>> BinarySearchTree(None).kth_smallest(1) is None   # Empty BST
        True
        >>> BinarySearchTree(10).kth_smallest(0)
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
        >>> bst.kth_smallest(2)
        5
        >>> bst.kth_smallest(3)
        7
        >>> bst.kth_smallest(5)
        11
        """
        if self._root is None:
            return None

        left_size = 0 if not self._left else self._left._calculate_size()

        if k < left_size:
            return self._left.kth_smallest(k)  # Search in the left subtree
        elif k == left_size:
            return self._root  # Current root is the kth smallest
        else:
            return self._right.kth_smallest(
                k - left_size - 1) if self._right else None

    def _calculate_size(self) -> int:
        """Helper method to calculate the size of the tree."""
        if self._root is None:
            return 0
        left_size = 0 if not self._left else self._left._calculate_size()
        right_size = 0 if not self._right else self._right._calculate_size()
        return 1 + left_size + right_size


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.

    Attributes:
    - _root:
        The item stored at this tree's root, or None if the tree is empty.
    - _subtrees:
        The list of all subtrees of this tree.

    Representation Invariants:
    - (self._root is None and self._subtrees == []) or self._root is not None
        # i.e. If self._root is None then self._subtrees is an empty list.
        # This setting of attributes represents an empty Tree.

    Note: self._subtrees may be empty when self._root is not None.
    This setting of attributes represents a tree consisting of just one
    node (a 'leaf')
    """
    _root: Any | None
    _subtrees: list[Tree]

    def __init__(self, root: Any | None, subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Preconditions:
            - (root is None and subtrees == []) or root is not None
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also write len(subtree) here
            return size

    def get_ith_postorder_item(self, i: int) -> Any | None:
        """Return the ith item in this Tree from a post-order traversal.

        Do not use any helpers aside from __len__ (and recursive calls to
        get_ith_postorder_item).

        >>> t1 = Tree(17, [])
        >>> t1.get_ith_postorder_item(0)
        17
        >>> t2 = Tree(-10, [])
        >>> t2.get_ith_postorder_item(0)
        -10
        >>> t3 = Tree(-11, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t3.get_ith_postorder_item(0)
        -2
        >>> t3.get_ith_postorder_item(1)
        10
        >>> t3.get_ith_postorder_item(2)
        -30
        >>> t3.get_ith_postorder_item(3)
        -11
        >>> t3.get_ith_postorder_item(4) is None
        True
        """
        if self.is_empty():
            return None

        for subtree in self._subtrees:
            subtree_len = len(subtree)
            if i < subtree_len:
                return subtree.get_ith_postorder_item(i)
            i -= subtree_len

        return self._root if i == 0 else None


if __name__ == '__main__':
    import doctest
    import python_ta

    doctest.testmod()

    python_ta.check_all(config={'max-line-length': 100})
