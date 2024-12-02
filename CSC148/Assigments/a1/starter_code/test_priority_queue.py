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
def test_given_example():
    pq = PriorityQueue(shorter)
    pq.add('fred')
    pq.add('arju')
    pq.add('monalisa')
    pq.add('hat')
    assert pq.remove() == 'hat'
    assert not pq.is_empty()


if __name__ == '__main__':
    pytest.main(['test_priority_queue.py'])
