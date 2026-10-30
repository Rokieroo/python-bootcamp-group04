"""W1-4: Translate C++ to Python – In-place insertion sort.

Difference from C++:
Unlike C++, Python does not need explicit type declarations.
Python uses // for integer division, not /.
Also, Python lists are dynamic and do not require size management.
"""


def insertion_sort(a: list[int]) -> list[int]:
    """Sort a list of integers in-place using insertion sort and return it."""
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


# Keep the original binary_search for reference
def binary_search(a: list[int], key: int) -> int:
    """Return the index of key in sorted list a, or -1 if not found.

    Difference from C++:
    Unlike C++, Python use // for integer division, not /
    Instead, / returns a float, which is not valid for indexing a list.
    Also, in C++, the formula mid = low + (high - low)/2 is used to avoid integer overflow of low + high.
    In Python, integers can be arbitrarily large, hence no need to worry about overflow.
    """
    low, high = 0, len(a) - 1
    while low <= high:
        mid = (low + high) // 2
        if a[mid] == key:
            return mid
        elif a[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    return -1
