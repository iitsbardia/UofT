"""
Assignment 1 - Domain classes (Task 2)
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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from distance_map import DistanceMap


class Parcel:
    # TODO: Implement this class!
    # It must be consistent with the Fleet class docstring examples below.
    pass


class Truck:
    # TODO: Implement this class!
    # It must be consistent with the Fleet class docstring examples below.
    pass


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: list[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        # TODO: Complete this method.
        pass

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        # TODO: Complete this method.
        pass

    # The format of the string that you return is up to you -- we will not test
    # it.
    def __str__(self) -> str:
        """Produce a string representation of this fleet
        """
        # TODO: Complete this method.
        pass

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        # TODO: Complete this method.
        pass

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        # TODO: Complete this method.
        pass

    def parcel_allocations(self) -> dict[int, list[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        # TODO: Complete this method.
        pass

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        # TODO: Complete this method.
        pass

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        # TODO: Complete this method.
        pass

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1424, 10, 'Toronto')
        >>> t3 = Truck(1425, 10, 'Toronto')
        >>> p3 = Parcel(2, 7, 'Buffalo', 'Hamilton')
        >>> t3.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.add_truck(t3)
        >>> f.average_fullness()
        60.0
        """
        # TODO: Complete this method.
        pass

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        # TODO: Complete this method.
        pass

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> t3 = Truck(6576, 10, 'Toronto')
        >>> p3 = Parcel(2, 5, 'Toronto', 'Montreal')
        >>> t3.pack(p3)
        True
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> m.add_distance('Toronto', 'Montreal', 12)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.add_truck(t3)
        >>> f.average_distance_travelled(m)
        21.0
        """
        # TODO: Complete this method.
        pass


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
