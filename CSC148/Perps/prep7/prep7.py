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

=== Module Description ===
Your task in this prep is to implement each of the following recursive functions
on nested lists, using the following steps for *Recursive Function Design*:

1.  Identify the recursive structure of the input (in this case, always a nested
    list), and write down the code template for nested lists:

    def f(obj: int | list) -> ...:
        if isinstance(obj, int):
            ...
        else:
            ...
            for sublist in obj:
                ... f(sublist) ...
            ...

2.  Implement the base case(s) directly (in this case, a single integer).
3.  Write down a concrete example with a somewhat complex argument, (in this
    case, a nested list with around 3 sub-nested-lists), and then write down
    the relevant recursive calls and what they should return.
4.  Determine how to combine the recursive calls to compute the correct output.
    Make sure you can express this in English first, and then implement your
    idea.

HINT: The implementations here should be similar to ones you've seen
before in the readings or comprehension questions.
"""
from python_ta.contracts import check_contracts


@check_contracts
def num_positives(obj: int | list) -> int:
    """Return the number of positive integers in <obj>.

    Remember, 0 is *not* positive.

    >>> num_positives(17)
    1
    >>> num_positives(-10)
    0
    >>> num_positives([1, -2, [-10, 2, [3], 4, -5], 4])
    5
    """
    if isinstance(obj, int):  # Base case: obj is an integer
        return 1 if obj > 0 else 0
    else:  # Recursive case: obj is a list
        count = 0
        for item in obj:
            count += num_positives(item)
        return count


@check_contracts
def nested_max(obj: int | list) -> int:
    """Return the maximum integer stored in nested list <obj>.

    Return 0 if <obj> does not contain any integers.

    Preconditions:
    - every integer in <obj> is greater than 0

    >>> nested_max(17)
    17
    >>> nested_max([1, 2, [1, 2, [3], 4, 5], 4])
    5
    >>> nested_max([[], []])
    0
    >>> nested_max([])
    0
    """
    if isinstance(obj, int):  # Base case: obj is an integer
        return obj
    elif isinstance(obj, list):  # Recursive case: obj is a list
        if not obj:  # If the list is empty, return 0
            return 0
        else:
            max_value = 0
            for item in obj:
                # Recursively check each item and update max_value
                max_value = max(max_value, nested_max(item))
            return max_value
    return 0  # Add this return to satisfy the linter


@check_contracts
def max_length(obj: int | list) -> int:
    """Return the maximum length of any list in nested list <obj>.

    The *maximum length* of a nested list is defined as:
    1. 0, if <obj> is a number.
    2. The maximum of len(obj) and the lengths of the nested lists contained
       in <obj>, if <obj> is a list.

    >>> max_length(17)
    0
    >>> max_length([1, 2, [1, 2], 4])
    4
    >>> max_length([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    if isinstance(obj, int):
        return 0
    elif isinstance(obj, list):
        # Start with the length of the current list
        max_value = len(obj)
        # Recursively find the maximum length in the nested lists
        for item in obj:
            max_value = max(max_value, max_length(item))
        return max_value
    return 0  # Add this return to satisfy the linter


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run prep7" or "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    import python_ta

    python_ta.check_all(config={'max-line-length': 100})
