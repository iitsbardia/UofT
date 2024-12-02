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

=== Module description ===
This module contains sample tests for Prep 6.
Complete the  in this file.

When writing a test case, make sure you create a new function, with its
name starting with "test_". For example:

def test_my_test_case():
    # Your test here

We will not check with file with PythonTA.
"""
from prep6 import LLStack, get_final_sentence


def test_llstack_multiple_push_pop() -> None:
    """Test LLStack when multiple pushes and pops are done."""
    stack = LLStack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2
    assert stack.pop() == 1


def test_get_final_sentence_examples() -> None:
    """Test get_final_sentence on the provided examples."""
    assert get_final_sentence(['hello', ' ', 'world']) == 'hello world'
    assert get_final_sentence(['hi', 'UNDO', 'hello', '!', ' ',
                               'UNDO', 'UNDO', ', ', 'world']) == 'hello, world'


def test_basic_functionality():
    """Test basic functionality of get_final_sentence with no complex scenarios."""
    # Test case 1: Simple sentence without any 'UNDO'
    assert get_final_sentence(['hello', ' ', 'world']) == 'hello world'

    # Test case 2: Sentence with a single 'UNDO' at the end
    assert get_final_sentence(['hello', 'UNDO']) == ''

    # Test case 3: Sentence with alternating words and 'UNDO'
    assert get_final_sentence(['first', 'UNDO', 'second', 'UNDO', 'third']) == 'third'


def test_edge_cases():
    """Test edge cases like empty list, only 'UNDO', etc."""
    # Test case 4: No input (empty list)
    assert get_final_sentence([]) == ''

    # Test case 5: Only 'UNDO's with no valid input
    assert get_final_sentence(['UNDO', 'UNDO', 'UNDO']) == ''

    # Test case 6: 'UNDO' with no words before
    assert get_final_sentence(['UNDO']) == ''

    # Test case 7: Single word with no 'UNDO'
    assert get_final_sentence(['word']) == 'word'

    # Test case 8: Single 'UNDO' with one word
    assert get_final_sentence(['word', 'UNDO']) == ''


def test_complex_undo_sequences():
    """Test sequences with multiple consecutive 'UNDO' commands."""
    # Test case 9: Consecutive 'UNDO's removing everything
    assert get_final_sentence(['one', 'two', 'three', 'UNDO', 'UNDO', 'UNDO']) == ''

    # Test case 10: Complex undo sequence with partial removal
    assert get_final_sentence(['this', ' ', 'is', ' ', 'a', ' ', ' ', 'test', 'UNDO', 'UNDO', 'undo']) == 'this is a undo'


def test_undo_at_different_positions():
    """Test cases where 'UNDO' appears at different positions in the input."""
    # Test case 11: 'UNDO' in the middle of the input
    assert get_final_sentence(['start', 'UNDO', 'middle', 'UNDO', 'end']) == 'end'

    # Test case 12: Sentence ending with 'UNDO' but not affecting the entire sentence
    assert get_final_sentence(['start', ' ', 'middle', 'UNDO', 'end']) == 'start end'

    # Test case 13: 'UNDO' at the beginning, removing the first word
    assert get_final_sentence(['UNDO', 'start', 'middle', 'end']) == 'startmiddleend'


def test_boundary_single_inputs():
    """Test boundary cases with single words or minimal inputs."""
    # Test case 14: Single word input
    assert get_final_sentence(['only']) == 'only'

    # Test case 15: Single character input
    assert get_final_sentence(['a']) == 'a'

    # Test case 16: Single character followed by 'UNDO'
    assert get_final_sentence(['a', 'UNDO']) == ''


if __name__ == '__main__':
    import pytest

    pytest.main(['prep6_starter_tests.py'])
