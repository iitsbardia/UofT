"""CSC148 Prep 5: Linked Lists

=== CSC148 Fall 2024 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu, Diane Horton and Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 David Liu, Diane Horton and Sophia Huynh

=== Module Description ===
This module contains sample tests for Prep 5. You may use these to test your
code.


When writing a test case, make sure you create a new function, with its
name starting with "test_". For example:

def test_my_test_case():
    # Your test here

We will not check with file with PythonTA.
"""
from prep5 import LinkedList, _Node


# You may also import the one_item and three_items helper functions.


################################################################################
# Part 2
# In this part of the prep, you are to write test cases for the __contains__
# method.
#
# We will run your tests on a correct version of prep5.py, as well as a version
# with an undisclosed bug in the __contains__ method. We will not give you
# hints as to what the bug is, so test thoroughly!
#
# When you are done, run the automated self-test on MarkUs. If you pass the
# test case named 'test_contains_test_cases': congratulations! You've found
# the bug, and you're done with this part.
#
# You may write as many test cases as you want. However, your test cases must
# fulfill the following requirements:
#     - All of your tests must pass on our correct version of prep5.py
#     - At least one of your tests must fail on the version with a bug.
#
# Make sure your tests all have different names that start with test_!
#
# You may assume __len__ and append work properly in both versions of prep5.py
# that we run your test cases on.
#
# Hint: Try to think about the different LinkedLists you could have:
#       - Consider both the length of the LinkedList, and its content.
#       - Consider the item being searched for: its position, and whether
#         it's in the LinkedList at all.
#       There are many different combinations for you to try.
################################################################################

# Below are provided sample test cases for your use. You are encouraged
# to add additional test cases.
# WARNING: THIS IS AN EXTREMELY INCOMPLETE SET OF TESTS!
# Add your own to practice writing tests and to be confident your code is
# correct.
def test_len_empty() -> None:
    """Test LinkedList.__len__ for an empty linked list."""
    lst = LinkedList()
    assert len(lst) == 0


def test_len_one_item() -> None:
    """Test LinkedList.__len__ on a list with one item."""
    lst = LinkedList()
    node1 = _Node(10)
    lst._first = node1
    assert len(lst) == 1


def test_len_three() -> None:
    """Test LinkedList.__len__ on a linked list of length 3."""
    lst = LinkedList()
    node1 = _Node(10)
    node2 = _Node(20)
    node3 = _Node(30)
    node1.next = node2
    node2.next = node3
    lst._first = node1

    assert len(lst) == 3


def test_contains_doctest() -> None:
    """Test LinkedList.__contains__ on the given doctest."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3
    lst._first = node1

    assert (2 in lst) is True
    assert (4 in lst) is False


def test_contains_empty_list() -> None:
    """Test LinkedList.__contains__ on an empty list."""
    lst = LinkedList()
    assert (1 in lst) is False


def test_contains_first_item() -> None:
    """Test LinkedList.__contains__ when the item is the first element."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3
    lst._first = node1

    assert (1 in lst) is True


def test_contains_middle_item() -> None:
    """Test LinkedList.__contains__ when the item is in the middle."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3
    lst._first = node1

    assert (2 in lst) is True


def test_contains_last_item() -> None:
    """Test LinkedList.__contains__ when the item is the last element."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3
    lst._first = node1

    assert (3 in lst) is True


def test_contains_not_in_list() -> None:
    """Test LinkedList.__contains__ when the item is not in the list."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3
    lst._first = node1

    assert (4 in lst) is False


def test_contains_single_item_matching() -> None:
    """Test LinkedList.__contains__ when the list has a single item matching."""
    lst = LinkedList()
    node1 = _Node(5)
    lst._first = node1

    assert (5 in lst) is True


def test_contains_single_item_not_matching() -> None:
    """Test LinkedList.__contains__ when the list has a single item not matching."""
    lst = LinkedList()
    node1 = _Node(5)
    lst._first = node1

    assert (10 in lst) is False


def test_contains_duplicate_items() -> None:
    """Test LinkedList.__contains__ when the list contains duplicate items."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(1)
    node1.next = node2
    node2.next = node3
    lst._first = node1

    assert (1 in lst) is True


def test_contains_none_item() -> None:
    """Test LinkedList.__contains__ when searching for None in a list containing None."""
    lst = LinkedList()
    node1 = _Node(None)
    node2 = _Node(2)
    lst._first = node1
    node1.next = node2

    assert (None in lst) is True


def test_contains_non_integer_items() -> None:
    """Test LinkedList.__contains__ when the list contains non-integer items."""
    lst = LinkedList()
    node1 = _Node("apple")
    node2 = _Node("banana")
    node1.next = node2
    lst._first = node1

    assert ("apple" in lst) is True
    assert ("banana" in lst) is True
    assert ("cherry" in lst) is False



def test_append_empty_list() -> None:
    """Test LinkedList.append on an empty list."""
    lst = LinkedList()
    lst.append(1)
    assert lst._first.item == 1
    assert lst._first.next is None


def test_append_one_item() -> None:
    """Test LinkedList.append on a list with one item."""
    lst = LinkedList()
    node1 = _Node(1)
    lst._first = node1
    lst.append(2)

    assert lst._first.item == 1
    assert lst._first.next.item == 2
    assert lst._first.next.next is None


def test_append_multiple_items() -> None:
    """Test LinkedList.append on a list with multiple items."""
    lst = LinkedList()
    node1 = _Node(1)
    node2 = _Node(2)
    node3 = _Node(3)
    node1.next = node2
    node2.next = node3
    lst._first = node1
    lst.append(4)

    assert lst._first.item == 1
    assert lst._first.next.item == 2
    assert lst._first.next.next.item == 3
    assert lst._first.next.next.next.item == 4
    assert lst._first.next.next.next.next is None


if __name__ == '__main__':
    import pytest

    pytest.main(['prep5_starter_tests.py'])
