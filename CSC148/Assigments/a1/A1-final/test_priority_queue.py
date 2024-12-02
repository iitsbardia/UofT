"""
Assignment 1 - Testing for priority queue (Task 3 a)
CSC148, Fall 2024

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 148 Teaching Team.

===== Module Description =====

This module contains tests for the PriorityQueue classes.
"""
import pytest
from container import PriorityQueue, shorter

# Add your test cases below - Make sure that they satisfy the criteria outlined
# on the handout.
# You can look at the provided tests in a1_starter_tests.py for examples.


# [MT] The following will be removed from the code provided to students
import pytest
from container import PriorityQueue, shorter


def test_given_example():
    pq = PriorityQueue(shorter)
    pq.add('fred')
    pq.add('arju')
    pq.add('monalisa')
    pq.add('hat')
    assert pq.remove() == 'hat'
    assert not pq.is_empty()


def test_is_empty():
    pq = PriorityQueue(shorter)
    assert pq.is_empty() is True


def test_add_single_item():
    pq = PriorityQueue(shorter)
    pq.add('apple')
    assert not pq.is_empty()
    assert pq.remove() == 'apple'


def test_priority_order():
    pq = PriorityQueue(shorter)
    pq.add('banana')
    pq.add('kiwi')
    pq.add('strawberry')
    pq.add('plum')
    assert pq.remove() == 'kiwi'
    assert pq.remove() == 'plum'
    assert pq.remove() == 'banana'
    assert pq.remove() == 'strawberry'


def test_remove_from_empty_queue():
    pq = PriorityQueue(shorter)
    with pytest.raises(IndexError):
        pq.remove()


def test_tie_breaking():
    pq = PriorityQueue(shorter)
    pq.add('cat')
    pq.add('dog')
    assert pq.remove() == 'cat'
    assert pq.remove() == 'dog'


def test_tie_breaking_same_length():
    pq = PriorityQueue(shorter)
    pq.add('bat')
    pq.add('cat')
    pq.add('mat')
    assert pq.remove() == 'bat'
    assert pq.remove() == 'cat'
    assert pq.remove() == 'mat'


def test_mixed_length_and_ties():
    pq = PriorityQueue(shorter)
    pq.add('apple')
    pq.add('fig')
    pq.add('banana')
    pq.add('date')
    pq.add('grape')
    pq.add('kiwi')

    assert pq.remove() == 'fig'
    assert pq.remove() == 'date'
    assert pq.remove() == 'kiwi'
    assert pq.remove() == 'apple'
    assert pq.remove() == 'grape'
    assert pq.remove() == 'banana'


if __name__ == '__main__':
    pytest.main(['test_priority_queue.py'])

