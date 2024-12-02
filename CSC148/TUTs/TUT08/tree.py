"""CSC148 Lab 8: Trees and Recursion

=== CSC148 Fall 2024 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains starter code for Lab 8.
Make sure you understand both the theoretical idea of trees, as well as how
we represent them in our Tree class.
"""
from __future__ import annotations
from typing import Any
from python_ta.contracts import check_contracts

import random  # For Task 2


@check_contracts
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
    _size: int

    def __init__(self, root: Any | None, subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees."""
        self._root = root
        self._subtrees = subtrees
        self._size = 1 if root is not None else 0
        for subtree in subtrees:
            self._size += subtree._size

    def __len__(self) -> int:
        """Return the number of items in this tree."""
        return self._size

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

    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this tree.

        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> 1 in t  # Same as t.__contains__(1)
        True
        >>> 5 in t
        True
        >>> 4 in t
        False
        """
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if item in subtree:
                    return True
            return False

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + str(self._root) + '\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                s += subtree._str_indented(depth + 1)
            return s

    def average(self) -> float:
        """Return the average of all the values in this tree.

        Return 0.0 if this tree is empty.

        Precondition: this is a tree of numbers.

        >>> Tree(None, []).average()
        0.0
        >>> t = Tree(13, [Tree(2, []), Tree(6, [])])
        >>> t.average()
        7.0
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, []), Tree(8, []), Tree(9, []),\
                          Tree(10, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.average()
        5.5
        """
        if self.is_empty():
            return 0.0
        else:
            total, count = self._sum_and_size()
            return total / count

    def _sum_and_size(self) -> tuple[int, int]:
        """Return a tuple (x,y) where:

        x is the total values in this tree, and
        y is the size of this tree.
        """
        if self.is_empty():
            return 0, 0
        else:
            total = self._root
            number = 1
            for subtree in self._subtrees:
                child_total, child_number = subtree._sum_and_size()
                total += child_total
                number += child_number
            return total, number

    # ------------------------------------------------------------------------
    # Lab Task 1: Non-mutating tree methods
    # ------------------------------------------------------------------------
    def branching_factor(self) -> float:
        """Return the average branching factor of this tree's internal values.

        Return 0.0 if this tree does not have internal values.

        >>> Tree(None, []).branching_factor()
        0.0
        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.branching_factor()
        2.0
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, []), Tree(8, []), Tree(9, []),\
                          Tree(10, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.branching_factor()
        3.0
        """
        if self.is_empty() or not self._subtrees:
            return 0.0

            # Initialize total branching and internal node counters
        total_branching = len(self._subtrees)
        internal_nodes = 1 if self._subtrees else 0

        for subtree in self._subtrees:
            subtree_branching, subtree_internal = subtree._branching_factor_helper()
            total_branching += subtree_branching
            internal_nodes += subtree_internal

        return total_branching / internal_nodes if internal_nodes > 0 else 0.0

    def _branching_factor_helper(self) -> tuple[int, int]:
        """Helper function to calculate total branching and internal nodes."""
        if self.is_empty() or not self._subtrees:
            return 0, 0  # No branching in an empty or leaf node

        # Current node contributes to branching and internal count
        branching_count = len(self._subtrees)
        internal_count = 1

        # Recurse through subtrees and accumulate branching and internal nodes
        for subtree in self._subtrees:
            subtree_branching, subtree_internal = subtree._branching_factor_helper()
            branching_count += subtree_branching
            internal_count += subtree_internal

        return branching_count, internal_count

    def items_at_depth(self, d: int) -> list:
        """Return a list of the values in this tree at the given depth.

        Preconditions:
            - d >= 1  # Depth 1 is the root of the tree

        We've provided some doctests for the empty and size-one tree cases.
        You'll want to write more doctests when working on the recursive case.

        >>> t1 = Tree(None, [])
        >>> t1.items_at_depth(2)
        []
        >>> t2 = Tree(5, [])
        >>> t2.items_at_depth(1)
        [5]
        """
        if d == 1:
            return [self._root] if not self.is_empty() else []
        else:
            items = []
            for subtree in self._subtrees:
                items.extend(subtree.items_at_depth(d - 1))
            return items

    # ------------------------------------------------------------------------
    # Lab Task 2: Tree insertion
    # ------------------------------------------------------------------------
    def insert(self, item: Any) -> None:
        """Insert <item> into this tree."""
        if self.is_empty():
            self._root = item
            self._size = 1
        elif not self._subtrees:
            # Add item as a new subtree if there are no subtrees
            new_subtree = Tree(item, [])
            self._subtrees.append(new_subtree)
            self._size += 1
        else:
            # Randomly insert into an existing subtree or add as a new subtree
            choice = random.randint(1, 3)
            if choice == 3:
                # Add item as a new subtree
                new_subtree = Tree(item, [])
                self._subtrees.append(new_subtree)
                self._size += 1
            else:
                # Recursively insert item in a randomly chosen subtree
                subtree = random.choice(self._subtrees)
                subtree.insert(item)
                self._size += 1


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['random'],
        'max-line-length': 100
    })
