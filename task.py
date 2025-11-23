"""Sorting algorithms comparison"""

import math
import random
import timeit
import matplotlib.pyplot as plt


def insertion_sort(lst):
    """Insertion sort algorithm"""
    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        while j >= 0 and key < lst[j]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key
    return lst


def merge(left, right):
    """Merge two sorted lists"""
    merged = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1

    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1

    return merged


def merge_sort(arr):
    """Merge sort algorithm"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    return merge(merge_sort(left_half), merge_sort(right_half))


def python_sort(lst):
    """Python in built sort algorithm for lists"""
    lst.sort()
    return lst


def python_sorted(lst):
    """Python in built sorted function"""
    return sorted(lst)


def benchmark(function, data, repeats):
    """Benchmark a sorting function with timeit module"""
    return timeit.timeit(lambda: function(data.copy()), number=repeats)


def compare_sorting_algorithms(list_sizes=None,
                               repeats=5,
                               seed=42,
                               value_range=(-10_000, 10_000)):
    """Compare sorting algorithms
    Args:
        list_sizes:  list of sizes of lists to compare
        repeats:     number of times to repeat the benchmark
        seed:        seed for the random number generator
        value_range: range of values for the random numbers
    Returns:
        list of results with time taken for each algorithm
    """
    if list_sizes is None:
        list_sizes = [10, 100, 1_000, 5_000]

    rng = random.Random(seed)
    results = []

    for size in list_sizes:
        base_data = [rng.randint(*value_range) for _ in range(size)]
        size_result = {
            "size": size,
            "insertion_sort": benchmark(insertion_sort, base_data, repeats),
            "merge_sort": benchmark(merge_sort, base_data, repeats),
            "list_sort": benchmark(python_sort, base_data, repeats),
            "sorted": benchmark(python_sorted, base_data, repeats),
        }
        results.append(size_result)

    return results


def _scale_theoretical_curve(values, reference):
    """Scale a list of values to a reference list for plotting
       in the same scale
    Args:
        values:    list of values to scale
        reference: list of reference values
    Returns:
        list of scaled values
    """
    if not values or not reference or values[-1] == 0:
        return values
    factor = reference[-1] / values[-1]
    return [value * factor for value in values]


def plot_sorting_results(results):
    """Plot sorting results
    Args:
        results: list of results with time taken for each algorithm
    """
    results = sorted(results, key=lambda entry: entry["size"])
    sizes = [entry["size"] for entry in results]
    insertion_times = [entry["insertion_sort"] for entry in results]
    merge_times = [entry["merge_sort"] for entry in results]
    list_sort_times = [entry["list_sort"] for entry in results]
    sorted_times = [entry["sorted"] for entry in results]

    insertion_complexity = [size**2 for size in sizes]
    merge_complexity = [size * math.log2(size) for size in sizes]

    insertion_complexity = _scale_theoretical_curve(
        insertion_complexity, insertion_times
    )
    merge_complexity = _scale_theoretical_curve(merge_complexity, merge_times)

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, insertion_times, "o-", label="insertion_sort (measured)")
    plt.plot(sizes, merge_times, "o-", label="merge_sort (measured)")
    plt.plot(sizes, list_sort_times, "o-", label="list.sort (measured)")
    plt.plot(sizes, sorted_times, "o-", label="sorted (measured)")
    plt.plot(sizes, insertion_complexity, "--", label="O(n²) reference")
    plt.plot(sizes, merge_complexity, "--", label="O(n log n) reference")

    plt.xlabel("List size (n)")
    plt.ylabel("Time (seconds, log scale)")
    plt.title("Sorting performance comparison")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    list_sizes = [10, 100, 1_000, 5_000, 10_000]
    comparison = compare_sorting_algorithms(list_sizes)
    for entry in comparison:
        size = entry["size"]
        print(f"Size: {size}")
        print(f"  insertion_sort: {entry['insertion_sort']:.6f} s")
        print(f"  merge_sort    : {entry['merge_sort']:.6f} s")
        print(f"  list.sort     : {entry['list_sort']:.6f} s")
        print(f"  sorted        : {entry['sorted']:.6f} s")
        print("-" * 40)

    plot_sorting_results(comparison)
