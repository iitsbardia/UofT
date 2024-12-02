"""CSC148 Lab 11: In-place Sorting Algorithms

=== CSC148 Fall 2024 ===
Sophia Huynh and Jonathan Calver
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains a variety of functions related to in-place sorting
algorithms that you will work through during this lab.
"""


def selection_sort(lst: list) -> list:
    """Return a sorted copy of lst, sorted using selection sort.

    >>> lst = [6, 1, 3, 4]
    >>> selection_sort(lst)
    [1, 3, 4, 6]
    """
    # This version of selection sort removes the smallest item
    # from the list at each iteration and builds a new list.
    lst_copy = lst[:]
    sorted_so_far = []

    while lst_copy != []:
        smallest = min(lst_copy)
        lst_copy.remove(smallest)
        sorted_so_far.append(smallest)

    return sorted_so_far


def _min_index(lst: list, i: int) -> int:
    """Return the index of the smallest item in lst[i:].

    In the case of ties, return the smaller index (i.e., the index that
    appears first).

    Preconditions:
        - 0 <= i <= len(lst) - 1
    """
    index_of_smallest_so_far = i

    for j in range(i + 1, len(lst)):
        if lst[j] < lst[index_of_smallest_so_far]:
            index_of_smallest_so_far = j

    return index_of_smallest_so_far


def in_place_selection_sort(lst: list) -> None:
    """Return a sorted copy of lst, sorted using selection sort.

    You may find the _min_index helper function helpful.

    >>> lst = [6, 1, 3, 4]
    >>> in_place_selection_sort(lst)
    >>> lst
    [1, 3, 4, 6]
    """
    # TODO: Implement this function.
    # You will want to swap with the smallest item in the "unsorted" partition
    # of the list at each iteration. The _min_index helper function should be
    # helpful.


def _in_place_partition(lst: list) -> int:
    """Mutate lst such that it's partitioned into smaller and bigger
    halves and returns the index of the pivot.

    >>> lst = [10, 3, 20, 5, -6, 30, 7]
    >>> _in_place_partition_indexed(lst, 0, 7)  # Pivot is 10
    4
    >>> lst[4]  # Note that 10 is at index 4
    10
    >>> set(lst[:4]) == {3, 5, -6, 7}
    True
    >>> set(lst[5:]) == {20, 30}
    True
    """
    # TODO: Implement this function.
    pivot = lst[0]


def _in_place_partition_indexed(lst: list, start: int, end: int) -> int:
    """Mutate lst such that it's partitioned into smaller and bigger
    halves and returns the index of the pivot.

    The partition should only apply to the slice [start:end]
    (Includes start, excludes end.)

    Preconditions:
        - 0 <= start <= end <= len(lst)

    >>> lst = [10, 3, 20, 5, -6, 30, 7]
    >>> _in_place_partition_indexed(lst, 0, 5)  # Pivot is 10
    3
    >>> lst[3]  # Note that 10 is at index 4
    10
    >>> set(lst[:3]) == {3, 5, -6}
    True
    >>> lst[4:] == [20, 30, 7]
    True
    """
    # TODO: Implement this function.
    pivot = lst[start]


def in_place_quicksort(lst: list) -> None:
    """Sort lst in place using quicksort.

    You will want to use the _in_place_partition_indexed helper.
    You may also want to make another helper function OR modify
    the function signature to take optional parameters.

    >>> lst = [6, 1, 3, 4]
    >>> in_place_quicksort(lst)
    >>> lst
    [1, 3, 4, 6]
    """
    # TODO: Implement this function.


def _merge_halves(lst: list) -> None:
    """Mutate lst by merging lst[:len(lst // 2)] and lst[len(lst // 2):]
    together.

    Preconditions:
        - lst[:len(lst)//2] is sorted
        - lst[len(lst)//2:] is sorted

    >>> lst = [1, 5, 2, 4]
    >>> _merge_halves(lst)
    >>> lst
    [1, 2, 4, 5]
    """
    # TODO: Implement this function.
    #       We have started the implementation for you.
    left = lst[:len(lst) // 2]
    right = lst[len(lst) // 2:]

    # TODO: Merge left and right together, replacing the
    #       values of lst starting at lst[0].
    # (i.e. lst[0] should be reassigned to the smaller of left[0] and right[0])


def _merge_indexed(lst: list, start: int, mid: int, end: int):
    """Mutate lst by merging lst[start:end] with lst[start:mid] and lst[mid:end].

    Preconditions:
        - lst[:len(lst)//2] is sorted
        - lst[len(lst)//2:] is sorted

    >>> lst = [1, 5, 2, 4, 9, 10, 8, 11]
    >>> _merge_indexed(lst, 0, 2, 4)
    >>> lst
    [1, 2, 4, 5, 9, 10, 8, 11]
    """
    # TODO: Implement this function.
    #       We have started the implementation for you.
    left = lst[start:mid]
    right = lst[mid:end]


def in_place_mergesort(lst: list) -> None:
    """Sort lst in place using mergesort.

    You will want to use the _merge_indexed helper.
    You may also want to make another helper function OR modify
    the function signature to take optional parameters.

    >>> lst = [6, 1, 3, 4]
    >>> in_place_mergesort(lst)
    >>> lst
    [1, 3, 4, 6]
    """
    # TODO: Implement this function.

# Implemented in-place sorting functions for full credit.

# In-place selection sort
def in_place_selection_sort(lst):
    for i in range(len(lst)):
        min_idx = _min_index(lst, i)
        lst[i], lst[min_idx] = lst[min_idx], lst[i]

# Partition the list for quicksort
def _in_place_partition(lst):
    pivot = lst[0]
    left = 1
    right = len(lst) - 1
    while left <= right:
        if lst[left] <= pivot:
            left += 1
        elif lst[right] > pivot:
            right -= 1
        else:
            lst[left], lst[right] = lst[right], lst[left]
            left += 1
            right -= 1
    lst[0], lst[right] = lst[right], lst[0]
    return right

# Partition the list for quicksort within a range
def _in_place_partition_indexed(lst, start, end):
    pivot = lst[start]
    left = start + 1
    right = end - 1
    while left <= right:
        if lst[left] <= pivot:
            left += 1
        elif lst[right] > pivot:
            right -= 1
        else:
            lst[left], lst[right] = lst[right], lst[left]
            left += 1
            right -= 1
    lst[start], lst[right] = lst[right], lst[start]
    return right

# In-place quicksort
def in_place_quicksort(lst, start=0, end=None):
    if end is None:
        end = len(lst)
    if start < end - 1:
        pivot_index = _in_place_partition_indexed(lst, start, end)
        in_place_quicksort(lst, start, pivot_index)
        in_place_quicksort(lst, pivot_index + 1, end)
