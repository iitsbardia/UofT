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
in the simulation: Parcel, Truck, and Fleet.
"""

from typing import List, Dict, Any
from distance_map import DistanceMap


class Parcel:
    """Represents a parcel in the delivery system."""
    parcel_id: Any
    volume: int
    source: str
    destination: str

    def __init__(self, parcel_id: Any, volume: int,
                 source: str, destination: str) -> None:
        self.parcel_id = parcel_id
        try:
            self.volume = int(volume)
        except ValueError:
            raise ValueError(f"Invalid volume '{volume}' for Parcel "
                             f"{parcel_id}. Volume must be an integer.")
        self.source = source
        self.destination = destination


class Truck:
    """Represents a truck in the delivery system."""
    truck_id: Any
    capacity: int
    remaining_capacity: int
    depot_location: str
    parcels: List[Parcel]
    route: List[str]
    parcel_count: int

    def __init__(self, truck_id: Any, capacity: int,
                 depot_location: str) -> None:
        self.truck_id = truck_id
        self.capacity = int(capacity)
        self.remaining_capacity = self.capacity
        self.depot_location = depot_location
        self.parcels = []
        self.route = [depot_location]
        self.parcel_count = 0

    def pack(self, parcel: Parcel) -> bool:
        """
        Add a parcel to the truck if there is enough capacity.
        Updates the route if the parcel's destination is not the last city.
        Returns True if the parcel is added successfully, False otherwise.
        """
        if self.remaining_capacity >= parcel.volume:
            self.parcels.append(parcel)
            self.remaining_capacity -= parcel.volume
            self.parcel_count += 1

            # Update route if the destination is not already the last city
            if self.route[-1] != parcel.destination:
                self.route.append(parcel.destination)
            return True
        return False

    def fullness(self) -> float:
        """Return the percentage of the truck's capacity used."""
        used_capacity = self.capacity - self.remaining_capacity
        return (used_capacity / self.capacity) * 100

    def total_distance(self, dmap: DistanceMap) -> int:
        """Return the total distance traveled by this truck
         based on its route."""
        total = 0
        for i in range(len(self.route) - 1):
            dist = dmap.distance(self.route[i], self.route[i + 1])
            if dist == -1:
                continue  # Skip
            total += dist

        if len(self.route) > 1:
            return_trip = dmap.distance(self.route[-1], self.route[0])
            if return_trip != -1:
                total += return_trip
        return total


class Fleet:
    """A fleet of trucks for making deliveries."""
    trucks: List[Truck]
    depot_location: str

    def __init__(self, depot_location: str = 'unknown') -> None:
        """Create a Fleet with no trucks."""
        self.trucks = []
        self.depot_location = depot_location

    def add_truck(self, truck: Truck) -> None:
        """Add a truck to this fleet."""
        self.trucks.append(truck)

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet."""
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet."""
        return sum(1 for truck in self.trucks if truck.parcels)

    def parcel_allocations(self) -> Dict[str, List[str]]:
        """Return a dictionary with truck IDs and their allocated
        parcel IDs."""
        allocations: Dict[str, List[str]] = {}
        for truck in self.trucks:
            allocations[truck.truck_id] = [parcel.parcel_id for parcel
                                           in truck.parcels]
        return allocations

    def total_unused_space(self) -> int:
        """Return the total unused space for all trucks in the fleet."""
        return sum(truck.remaining_capacity for truck in self.trucks)

    def calculate_unused_trucks(self) -> int:
        """Return the number of unused trucks (those with no parcels)."""
        return self.num_trucks() - self.num_nonempty_trucks()

    def average_fullness(self) -> float:
        """Return the average fullness of all non-empty trucks."""
        non_empty_trucks = [truck for truck in self.trucks if truck.parcels]
        if non_empty_trucks:
            total_fullness = sum(truck.fullness() for truck
                                 in non_empty_trucks)
            return total_fullness / len(non_empty_trucks)
        return 0.0

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by trucks in this fleet."""
        return sum(truck.total_distance(dmap) for truck in self.trucks)

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """
        Return the average distance travelled by trucks that have travelled.
        """
        traveled_trucks = [truck for truck in self.trucks if truck.parcels]
        if traveled_trucks:
            total_distance = self.total_distance_travelled(dmap)
            return total_distance / len(traveled_trucks)
        return 0.0


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
