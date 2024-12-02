"""CSC148 Prep 7: Recursion

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

=== Module description ===
This module contains sample tests for Prep 7.

Complete the TODO in this file.

When writing a test case, make sure you create a new function, with its
name starting with "test_". For example:

def test_my_test_case():
    # Your test here
"""
from prep7 import num_positives, nested_max, max_length


def test_num_positives_single_int_positive() -> None:
    """Test num_positives with a single positive integer."""
    assert num_positives(17) == 1


def test_num_positives_single_int_negative() -> None:
    """Test num_positives with a single negative integer."""
    assert num_positives(-10) == 0


def test_num_positives_mixed_nested_list() -> None:
    """Test num_positives with a nested list containing positive and negative integers."""
    assert num_positives([1, -2, [-10, 2, [3], 4, -5], 4]) == 5


def test_num_positives_empty_list() -> None:
    """Test num_positives with an empty list."""
    assert num_positives([]) == 0


def test_nested_max_single_int() -> None:
    """Test nested_max with a single integer."""
    assert nested_max(17) == 17


def test_nested_max_nested_list() -> None:
    """Test nested_max with a nested list of integers."""
    assert nested_max([1, 2, [1, 2, [3], 4, 5], 4]) == 5


def test_nested_max_all_zeros() -> None:
    """Test nested_max with a list of zeros."""
    assert nested_max([0, [0, 0], 0]) == 0


def test_nested_max_empty_list() -> None:
    """Test nested_max with an empty list."""
    assert nested_max([]) == 0


def test_max_length_single_int() -> None:
    """Test max_length with a single integer."""
    assert max_length(17) == 0


def test_max_length_empty_list() -> None:
    """Test max_length with an empty list."""
    assert max_length([]) == 0


def test_max_length_flat_list() -> None:
    """Test max_length with a flat list of integers."""
    assert max_length([1, 2, 3, 4]) == 4


def test_max_length_nested_list() -> None:
    """Test max_length with a nested list."""
    assert max_length([1, 2, [1, 2], 4]) == 4


def test_num_positives_doctest_example() -> None:
    """Test num_positive on one of the given doctest examples."""
    assert num_positives([1, -2, [-10, 2, [3], 4, -5], 4]) == 5


def test_nested_max_doctest_example() -> None:
    """Test nested_max on one of the given doctest examples."""
    assert nested_max([1, 2, [1, 2, [3], 4, 5], 4]) == 5


def test_max_length_doctest_example() -> None:
    """Test max_length on one of the given doctest examples."""
    assert max_length([1, 2, [1, 2], 4]) == 4


if __name__ == '__main__':
    import pytest

    pytest.main(['prep7_starter_tests.py'])
