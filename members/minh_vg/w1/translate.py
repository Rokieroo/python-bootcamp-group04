"""W1-4: Translate C++ to Python – In-place insertion sort.

Unlike C++'s std::vector<int>, a Python list supports dynamic resizing and
does not require explicit memory management. The sort is performed in-place
by shifting elements, identical to the C++ algorithm.
"""

from collections.abc import Iterable, Mapping, Sequence
from typing import TypeVar

Node = TypeVar("Node", int, str)


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


# Keep the original graph traversal code for reference
def build_graph(
    edges: Iterable[tuple[Node, Node]], directed: bool = False,
    nodes: Iterable[Node] | None = None,
) -> dict[Node, list[Node]]:
    """Build sorted, duplicate-free adjacency lists, including isolated nodes."""
    neighbors = {node: set() for node in nodes or []}
    for source, target in edges:
        neighbors.setdefault(source, set()).add(target)
        neighbors.setdefault(target, set())
        if not directed:
            neighbors[target].add(source)
    return {node: sorted(adjacent) for node, adjacent in neighbors.items()}


def dfs(graph: Mapping[Node, Sequence[Node]], start: Node) -> list[Node]:
    """Recursively visit reachable nodes, visiting smaller neighbors first."""
    if start not in graph:
        raise ValueError("start must be a node in the graph")

    visited = set()
    order = []

    def visit(node: Node) -> None:
        """Visit one unseen node and its reachable neighbors in sorted order."""
        visited.add(node)
        order.append(node)
        for neighbor in sorted(graph.get(node, [])):
            if neighbor not in visited:
                visit(neighbor)

    visit(start)
    return order


def dfs_iterative(graph: Mapping[Node, Sequence[Node]], start: Node) -> list[Node]:
    """Match recursive DFS using a stack, without Python's recursion limit."""
    if start not in graph:
        raise ValueError("start must be a node in the graph")
    visited = set()
    order = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        stack.extend(sorted(graph.get(node, []), reverse=True))
    return order
