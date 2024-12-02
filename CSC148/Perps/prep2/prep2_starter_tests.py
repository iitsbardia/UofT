"""CSC148 Prep 2: Object Oriented Programming

=== CSC148 Fall 2024 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu, Diane Horton, and Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 David Liu, Diane Horton, and Sophia Huynh

=== Module Description ===
This module contains sample tests for Prep 2.
Complete the
There is also a task inside prep2.py.
Make sure to look at that file and complete the

We suggest you also add your own tests to practice writing tests and
to be confident your code is correct.

When writing a test case, make sure you create a new function, with its
name starting with "test_". For example:

def test_my_test_case():
    # Your test here

All test cases must have different names (i.e. you cannot have two tests
named test_my_test_case).

NOTE: We will not be checking this file with PythonTA. So even though you
will submit both this file and prep2.py, only prep2.py will be checked
with PythonTA for grading purposes.
"""
from hypothesis import given
from hypothesis.strategies import integers
from datetime import date
from prep2 import Spinner
from prep2_coverage_example import coverage_example


################################################################################
# Part 3
# In this part, you will be writing tests such that you have full coverage of
# prep2_coverage_function.py
################################################################################
def test_coverage_provided():
    """Call coverage_example() on a single example.

    This call covers the branch where x == 0
    """
    assert coverage_example(0) is True

def test_coverage_negative():
    """Call coverage_example() on a single negative example.

    This call covers the branch where x < 0
    """
    assert coverage_example(-100) is False

def test_coverage_special_examples():
    """Call coverage_example() on three specific examples.

    This call covers the branch where x is in [1, 10, 100]
    """
    assert coverage_example(1) is True
    assert coverage_example(10) is True
    assert coverage_example(100) is True

def test_coverage_default():
    """Call coverage_example() on examples that don't match any specific condition.

    This call covers the else branch
    """
    assert coverage_example(299) is False
    assert coverage_example(50) is False
    assert coverage_example(2) is False


################################################################################
# Sample test cases below
#
# Use the below test cases as an example for writing your own test cases,
# and as a start to testing your prep2.py code.
#
# The self-test on MarkUs runs the tests below, along with a few others.
# Make sure you run the self-test after submitting your code!
#
# WARNING: THIS IS CURRENTLY AN EXTREMELY INCOMPLETE SET OF TESTS!
# We will test your code on a much more thorough set of tests!
# We encourage you to add your own test cases to this file.
################################################################################
def test_doctest() -> None:
    """Test the given doctest in the Spinner class docstring."""
    spinner = Spinner(8)

    spinner.spin(4)
    assert spinner.position == 4

    spinner.spin(2)
    assert spinner.position == 6

    spinner.spin(2)
    assert spinner.position == 0


# This is a hypothesis test; it generates a random integer to use as input,
# so that we don't need to hard-code a specific number of slots in the test.
# For more information on hypothesis (one of the testing libraries we're using),
# please see
# https://www.teach.cs.toronto.edu/~csc148h/winter/notes/testing/hypothesis.html
@given(slots=integers(min_value=1))
def test_new_spinner_position(slots: int) -> None:
    """Test that the position of a new spinner is always 0."""
    spinner = Spinner(slots)
    assert spinner.position == 0


def test_unlike_doctest() -> None:
    """Test the given doctest in the unlike method of Tweet."""
    from prep2 import Tweet
    tweet = Tweet('Sophia', date(2021, 1, 1), 'Happy new year!')
    tweet.like(5)
    assert tweet.likes == 5
    tweet.unlike()
    assert tweet.likes == 4


if __name__ == '__main__':
    import pytest

    pytest.main(['prep2_starter_tests.py'])
