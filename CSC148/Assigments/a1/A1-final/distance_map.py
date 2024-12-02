"""
Assignment 1 - Distance map (Task 1)
CSC148, Fall 2024

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""


class DistanceMap:
    """
    A class that stores and retrieves distances between pairs of cities.
    """
    _distances: dict[tuple[str, str], int]

    def __init__(self) -> None:
        """Initialize an empty DistanceMap."""
        self._distances = {}

    def add_distance(self, city_a: str, city_b: str, distance_ab: int,
                     distance_ba: int = None) -> None:
        """
        Add the distance between two cities.

        If distance_ba is provided, it sets an asymmetrical distance
        (different distances from city_a to city_b and from city_b to city_a).
        If not, it assumes symmetry.
        """
        self._distances[(city_a, city_b)] = distance_ab
        if distance_ba is not None:
            self._distances[(city_b, city_a)] = distance_ba
        else:
            self._distances[(city_b, city_a)] = distance_ab

    def distance(self, city_a: str, city_b: str) -> int:
        """
        Return the distance from city_a to city_b, or -1 if not stored.
        """
        return self._distances.get((city_a, city_b), -1)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
