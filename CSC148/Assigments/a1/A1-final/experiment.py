"""
Module for scheduling experiments with parcels and trucks.

This module sets up an experiment based on a given configuration,
runs the experiment, generates statistics, and optionally reports them.
"""

from typing import Union
import json
from scheduler import RandomScheduler, GreedyScheduler, Scheduler
from domain import Parcel, Truck, Fleet
from distance_map import DistanceMap


class SchedulingExperiment:
    """An experiment in scheduling parcels for delivery."""

    scheduler: Scheduler
    parcels: list[Parcel]
    fleet: Fleet
    dmap: DistanceMap
    _stats: dict[str, Union[int, float]]
    _unscheduled: list[Parcel]

    def __init__(self, config: dict[str, Union[str, bool]]) -> None:
        """Initialize a new experiment from the configuration dictionary."""

        if config['algorithm'] == 'random':
            self.scheduler = RandomScheduler()
        elif config['algorithm'] == 'greedy':
            self.scheduler = GreedyScheduler(config)
        else:
            raise ValueError("Invalid algorithm specified in config.")

        self.parcels = read_parcels(config['parcel_file'])
        self.fleet = read_trucks(config['truck_file'],
                                 config['depot_location'])
        self.dmap = read_distance_map(config['map_file'])

        # Initialize statistics and unscheduled parcels tracking
        self._stats = {}
        self._unscheduled = []

    def run(self, report: bool = False) -> dict[str, Union[int, float]]:
        """Run the experiment and return statistics on the outcome."""

        # Schedule parcels and store unscheduled parcels
        self._unscheduled = self.scheduler.schedule(self.parcels,
                                                    self.fleet.trucks)
        self._compute_stats()

        if report:
            self._print_report()

        return self._stats

    def _compute_stats(self) -> None:
        """Compute the statistics for this experiment and store in
        self._stats."""

        self._stats['fleet'] = self.fleet.num_trucks()
        self._stats['unused_trucks'] = self.fleet.calculate_unused_trucks()

        used_trucks = [truck for truck in self.fleet.trucks if truck.parcels]
        if used_trucks:
            self._stats['avg_distance'] = sum(
                truck.total_distance(self.dmap) for truck in used_trucks
            ) / len(used_trucks)

            self._stats['avg_fullness'] = sum(
                truck.fullness() for truck in used_trucks
            ) / len(used_trucks)

            # Total unused space in all used trucks
            self._stats['unused_space'] = sum(
                truck.remaining_capacity for truck in used_trucks
            )
        else:
            # Default values if no trucks are used
            self._stats['avg_distance'] = 0.0
            self._stats['avg_fullness'] = 0.0
            self._stats['unused_space'] = 0

        # Track number of unscheduled parcels
        self._stats['unscheduled'] = len(self._unscheduled)

    def _print_report(self) -> None:
        """Report on the statistics for this experiment."""

        print("Scheduling Experiment Report:")
        print(f"  Total trucks in fleet: {self._stats['fleet']}")
        print(f"  Unused trucks: {self._stats['unused_trucks']}")
        print(f"  Average distance traveled by used trucks: "
              f"{self._stats['avg_distance']: .2f}")
        print(f"  Average fullness of used trucks: "
              f"{self._stats['avg_fullness']: .2f}%")
        print(f"  Total unused space in used trucks: "
              f"{self._stats['unused_space']} units")
        print(f"  Number of unscheduled parcels: "
              f"{self._stats['unscheduled']}")


def read_parcels(parcel_file: str) -> list[Parcel]:
    """Read parcel data from <parcel_file> and return a list of Parcel
    objects."""
    parcels = []
    with open(parcel_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            pid = int(tokens[0].strip())
            source = tokens[1].strip()
            destination = tokens[2].strip()
            volume = int(tokens[3].strip())
            parcels.append(Parcel(parcel_id=pid, volume=volume, source=source,
                                  destination=destination))
    return parcels


def read_distance_map(distance_map_file: str) -> DistanceMap:
    """Read distance data from <distance_map_file> and return a DistanceMap."""
    dmap = DistanceMap()
    with open(distance_map_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            c1 = tokens[0].strip()
            c2 = tokens[1].strip()
            distance1 = int(tokens[2].strip())
            if len(tokens) == 4:
                distance2 = int(tokens[3].strip())
            else:
                distance2 = distance1
            dmap.add_distance(c1, c2, distance1, distance2)
    return dmap


def read_trucks(truck_file: str, depot_location: str) -> Fleet:
    """Read truck data from <truck_file> and return a Fleet containing these
    trucks."""
    fleet = Fleet(depot_location)
    with open(truck_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            tid = int(tokens[0].strip())
            capacity = int(tokens[1].strip())
            truck = Truck(truck_id=tid, capacity=capacity,
                          depot_location=depot_location)
            fleet.add_truck(truck)
    return fleet


def simple_check(config_file: str) -> None:
    """Configure and run a single experiment on the scheduling problem defined
     in <config_file>."""
    with open(config_file, 'r') as file:
        configuration = json.load(file)

    experiment = SchedulingExperiment(configuration)
    experiment.run(report=True)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['read_parcels', 'read_distance_map', 'read_trucks',
                       'SchedulingExperiment._print_report', 'simple_check'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'json', 'scheduler', 'domain',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })

    simple_check('data/demo.json')
