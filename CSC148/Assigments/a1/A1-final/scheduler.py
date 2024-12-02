"""
Assignment 1 - Scheduling algorithms (Task 4)
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

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import Callable, List, Dict, Union
from random import shuffle, choice
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class. Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck]) \
            -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>."""
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """Randomly assigns parcels to trucks that have enough space."""
    config: Dict[str, Union[str, int, bool]]

    def __init__(self) -> None:
        pass

    def schedule(self, parcels: List[Parcel], trucks: List[Truck]) \
            -> List[Parcel]:
        """Assign parcels randomly to available trucks."""
        unscheduled = []
        shuffle(parcels)

        for parcel in parcels:
            eligible_trucks = [truck for truck in trucks
                               if truck.remaining_capacity >= parcel.volume]
            if eligible_trucks:
                chosen_truck = choice(eligible_trucks)
                if not chosen_truck.pack(parcel):
                    unscheduled.append(parcel)
            else:
                unscheduled.append(parcel)

        return unscheduled


class GreedyScheduler(Scheduler):
    """Greedy scheduler with configurable parcel order and truck choice."""
    config: Dict[str, Union[str, int, bool]]

    def __init__(self, config: dict) -> None:
        self.config = config

    def schedule(self, parcels: List[Parcel], trucks: List[Truck]) \
            -> List[Parcel]:
        """Assign parcels to trucks using a greedy algorithm based
        on config."""
        unscheduled = []

        parcel_priority_fn = self._get_priority_function()
        parcels_queue = PriorityQueue(parcel_priority_fn)
        for parcel in parcels:
            parcels_queue.add(parcel)

        while not parcels_queue.is_empty():
            parcel = parcels_queue.remove()
            eligible_trucks = [truck for truck in trucks
                               if truck.remaining_capacity >= parcel.volume]
            eligible_trucks = (self._filter_trucks_by_destination
                               (eligible_trucks, parcel))

            if eligible_trucks:
                chosen_truck = self._choose_best_truck(eligible_trucks)
                if not chosen_truck.pack(parcel):
                    unscheduled.append(parcel)
            else:
                unscheduled.append(parcel)

        return unscheduled

    def _get_priority_function(self) -> Callable[[Parcel, Parcel], bool]:
        """Return a comparison function based on the config that compares
        two parcels."""
        if self.config['parcel_priority'] == 'volume':
            if self.config['parcel_order'] == 'non-decreasing':
                return lambda p1, p2: p1.volume < p2.volume
            else:
                return lambda p1, p2: p1.volume > p2.volume
        elif self.config['parcel_priority'] == 'destination':
            if self.config['parcel_order'] == 'non-decreasing':
                return lambda p1, p2: p1.destination < p2.destination
            else:
                return lambda p1, p2: p1.destination > p2.destination
        return lambda p1, p2: False  # Default return for function completeness

    @staticmethod
    def _filter_trucks_by_destination(trucks: List[Truck], parcel: Parcel) \
            -> List[Truck]:
        """Filters trucks that already have the parcel's destination as
        the last stop."""
        end_destination_trucks = [truck for truck in trucks
                                  if truck.route
                                  and truck.route[-1] == parcel.destination]
        return end_destination_trucks if end_destination_trucks else trucks

    def _choose_best_truck(self, trucks: List[Truck]) -> Truck:
        """Chooses the best truck based on available space, as per config."""
        if self.config['truck_order'] == 'non-increasing':
            return max(trucks, key=lambda truck: truck.remaining_capacity)
        else:
            return min(trucks, key=lambda truck: truck.remaining_capacity)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing', 'random',
                                   'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
