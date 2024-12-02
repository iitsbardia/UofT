
import random
import sys
from timeit import timeit

from bst import BinarySearchTree

SIZES = [100, 200, 400, 800, 1600]

def insert_delete_all(items: list[int]) -> None:
    """Insert the items in <items> into an empty BinarySearchTree, and then
    remove them in the same order they were added.
    """
    bst = BinarySearchTree()
    for item in items:
        bst.insert(item)
    for item in items:
        bst.delete(item)

def get_items(size: int, is_sorted: bool) -> list[int]:
    """Return a list of <size> items."""
    items = list(range(size))
    if not is_sorted:
        random.shuffle(items)

    return items

def time_experiment():
    """Run the timing experiment on insert_delete_all for various BST sizes."""
    sys.setrecursionlimit(2000)

    random_times = []
    for size in SIZES:
        lst = get_items(size, False)
        time = timeit('insert_delete_all(lst)', number=10, globals={**globals(), 'lst': lst})
        random_times.append(time)
        print(f'Random list of size {size:>7}, time {round(time, 6)}')

    sorted_times = []
    for size in SIZES:
        lst = get_items(size, True)
        time = timeit('insert_delete_all(lst)', number=10, globals={**globals(), 'lst': lst})
        sorted_times.append(time)
        print(f'Sorted list of size {size:>7}, time {round(time, 6)}')

    return random_times, sorted_times

def plot_experiment():
    """Run the experiment and plot the times in a graph."""
    import matplotlib.pyplot as plt

    random_time, sorted_times = time_experiment()

    (start_plt,) = plt.plot(SIZES, random_time, 'ro')
    start_plt.set_label("Random list")

    (end_plt,) = plt.plot(SIZES, sorted_times, 'bo')
    end_plt.set_label("Sorted list")

    plt.legend()
    plt.xlabel("Size")
    plt.ylabel("Average Time (μs)")

    plt.show()

if __name__ == '__main__':
    plot_experiment()
