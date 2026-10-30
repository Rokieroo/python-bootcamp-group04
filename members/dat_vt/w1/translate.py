"""W1-4: Translate C++ to Python – Binary search.

Difference from C++:
Unlike C++, Python uses // for integer division instead of /.
Python integers can be arbitrarily large, so there is no overflow concern
with (low + high) // 2.
"""


def binary_search(a: list[int], key: int) -> int:
    """Return the index of key in sorted list a, or -1 if not found."""
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


if __name__ == "__main__":
    user_input = input("Please input integers separated by spaces: ")
    nums = [int(x) for x in user_input.split()]
    target = int(input("Enter the target: "))
    print(binary_search(nums, target))