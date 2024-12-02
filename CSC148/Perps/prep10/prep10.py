"""CSC148 Prep 10: Recursive Sorting Algorithms

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
Copyright (c) 2021 David Liu and Diane Horton

=== Module Description ===
This file includes the recursive sorting algorithms from this week's prep
readings, and two short programming exercises to extend your learning about
these algorithms in different ways.
"""
from typing import Any
from python_ta.contracts import check_contracts


################################################################################
# Mergesort and Quicksort
################################################################################
@check_contracts
def mergesort(lst: list) -> list:
    """Return a sorted list with the same elements as <lst>.

    This is a *non-mutating* version of mergesort; it does not mutate the
    input list.

    >>> mergesort([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    if len(lst) < 2:
        return lst[:]
    else:
        # Divide the list into two parts, and sort them recursively.
        mid = len(lst) // 2
        left_sorted = mergesort(lst[:mid])
        right_sorted = mergesort(lst[mid:])

        # Merge the two sorted halves. Need a helper here!
        return _merge(left_sorted, right_sorted)


@check_contracts
def _merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Preconditions:
        - sorted(lst1) == lst1
        - sorted(lst2) == lst2
    """
    index1 = 0
    index2 = 0
    merged = []
    while index1 < len(lst1) and index2 < len(lst2):
        if lst1[index1] <= lst2[index2]:
            merged.append(lst1[index1])
            index1 += 1
        else:
            merged.append(lst2[index2])
            index2 += 1

    # Now either index1 == len(lst1) or index2 == len(lst2).

    # The remaining elements of the other list
    # can all be added to the end of <merged>.
    # Note that at most ONE of lst1[index1:] and lst2[index2:]
    # is non-empty, but to keep the code simple, we include both.
    return merged + lst1[index1:] + lst2[index2:]


@check_contracts
def quicksort(lst: list) -> list:
    """Return a sorted list with the same elements as <lst>.

    This is a *non-mutating* version of quicksort; it does not mutate the
    input list.

    >>> quicksort([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    if len(lst) < 2:
        return lst[:]
    else:
        # Pick pivot to be first element.
        # Could make lots of other choices here (e.g., last, random)
        pivot = lst[0]

        # Partition rest of list into two halves
        smaller, bigger = _partition(lst[1:], pivot)

        # Recurse on each partition
        smaller_sorted = quicksort(smaller)
        bigger_sorted = quicksort(bigger)

        # Return! Notice the simple combining step
        return smaller_sorted + [pivot] + bigger_sorted


@check_contracts
def _partition(lst: list, pivot: Any) -> tuple[list, list]:
    """Return a partition of <lst> with the chosen pivot.

    Return two lists, where the first contains the items in <lst>
    that are <= pivot, and the second is the items in <lst> that are > pivot.
    """
    smaller = []
    bigger = []

    for item in lst:
        if item <= pivot:
            smaller.append(item)
        else:
            bigger.append(item)

    return smaller, bigger


@check_contracts
def mergesort3(lst: list) -> list:
    """Return a sorted version of <lst> using three-way mergesort.

    >>> mergesort3([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    if len(lst) < 2:
        return lst[:]
    elif len(lst) == 2:
        return [min(lst), max(lst)]
    else:
        # Divide the list into three nearly equal parts
        third = len(lst) // 3
        left_sorted = mergesort3(lst[:third])
        middle_sorted = mergesort3(lst[third:2 * third])
        right_sorted = mergesort3(lst[2 * third:])

        # Merge the three sorted parts
        return merge3(left_sorted, middle_sorted, right_sorted)


@check_contracts
def merge3(lst1: list, lst2: list, lst3: list) -> list:
    """Return a sorted list with the elements in the given input lists.

    Preconditions:
        - sorted(lst1) == lst1
        - sorted(lst2) == lst2
        - sorted(lst3) == lst3
    """
    index1 = index2 = index3 = 0
    merged = []

    # Merge until one list is exhausted
    while index1 < len(lst1) and index2 < len(lst2) and index3 < len(lst3):
        if lst1[index1] <= lst2[index2] and lst1[index1] <= lst3[index3]:
            merged.append(lst1[index1])
            index1 += 1
        elif lst2[index2] <= lst1[index1] and lst2[index2] <= lst3[index3]:
            merged.append(lst2[index2])
            index2 += 1
        else:
            merged.append(lst3[index3])
            index3 += 1

    # Use _merge to combine the remaining elements of the two non-exhausted lists
    if index1 < len(lst1):
        return merged + _merge(lst1[index1:], _merge(lst2[index2:], lst3[index3:]))
    elif index2 < len(lst2):
        return merged + _merge(lst2[index2:], lst3[index3:])
    else:
        return merged + lst3[index3:]


@check_contracts
def kth_smallest(lst: list, k: int) -> Any:
    """Return the <k>-th smallest element in <lst>.

    >>> kth_smallest([10, 20, -4, 3], 0)
    -4
    >>> kth_smallest([10, 20, -4, 3], 2)
    10
    """
    if k < 0 or k >= len(lst):
        raise IndexError("k is out of bounds")

    pivot = lst[0]
    smaller, bigger = _partition(lst[1:], pivot)

    if k < len(smaller):
        # The k-th smallest element is in the smaller partition
        return kth_smallest(smaller, k)
    elif k == len(smaller):
        # The k-th smallest element is the pivot
        return pivot
    else:
        # The k-th smallest element is in the bigger partition
        return kth_smallest(bigger, k - len(smaller) - 1)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={'max-line-length': 100})
