"""CSC148 Prep 6: Review

=== CSC148 Fall 2024 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Sophia Huynh

=== Module Description ===
This module contains various tasks for you to complete. In particular:
    1) Implementing the LLStack class
    2) Implementing the get_final_sentence() function

Additionally, there is a task in prep6_starter_tests.py!

The provided self-test on MarkUs is the FULL test suite for this week!
This is a more robust set of tests, and there are no hidden test cases.

Your grade will correspond to the number of test cases passed. If you
pass all of them, then you will receive full marks for this prep.
As such, any unspecified behaviour that is not in the self-test is left
as a design decision for you.

While style will NOT be checked for this lab, you should still include
documentation and type annotations where relevant.
"""
from __future__ import annotations
from typing import Any


class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    Attributes:
    - item:
        The data stored in this node.
    - next:
        The next node in the list, or None if there are no more nodes.
    """
    item: Any
    next: _Node | None

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class EmptyStackError(Exception):
    """Exception raised when calling pop on an empty stack."""

    def __str__(self) -> str:
        """Return a string representation of this error."""
        return 'You called pop on an empty stack.'


class StackADT:
    """A generalized abstract class for Stacks.

    Your LLStack class should implement all methods in this class.
    """

    def pop(self) -> Any:
        """Return and remove the top of the Stack."""
        raise NotImplementedError

    def push(self, item: Any) -> Any:
        """Adds <item> to the top of the Stack."""
        raise NotImplementedError

    def is_empty(self) -> Any:
        """Return True iff this Stack is empty."""
        raise NotImplementedError


class LLStack(StackADT):
    _top: _Node | None

    def __init__(self) -> None:
        """Initialize an empty linked list stack."""
        self._top = None

    def push(self, item: Any) -> None:
        """Push a new item onto the stack."""
        new_node = _Node(item)
        new_node.next = self._top
        self._top = new_node

    def pop(self) -> Any:
        """Pop the top item from the stack and return it."""
        if self._top is None:
            raise EmptyStackError
        item = self._top.item
        self._top = self._top.next
        return item

    def is_empty(self) -> bool:
        """Return True if the stack is empty, False otherwise."""
        return self._top is None


def get_final_sentence(lst: list[str]) -> str:
    ll = LLStack()

    for word in lst:
        if word == 'UNDO':
            if not ll.is_empty():
                ll.pop()
        else:
            ll.push(word)

    result = []
    while not ll.is_empty():
        result.append(ll.pop())

    return ''.join(reversed(result))

x`xmlx  
if __name__ == '__main__':
    import pytest
    import coverage

    # This creates a Coverage() object and starts recording information
    # about which lines have been run in my_functions.py
    cov = coverage.Coverage(include=['prep6.py'])
    cov.start()

    # This line runs the pytest cases in test_my_functions.py
    pytest.main(['prep6_starter_tests.py'])

    # These lines stop recording information and saves it
    cov.stop()
    cov.save()

    # The line below will print the report to the Python Console.
    cov.report()

    # The line below will generate a folder called htmlcov
    # Open the index.html page to see the coverage report. You can
    # click on the "my_functions.py" module there to see
    # which lines might be missing.
    cov.html_report()
