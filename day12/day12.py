#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/12
#

"""
The idea is to parse the input heightmap, convert each height which are letter to a numerical value. My convention is:
 - the current position has a value of 0 (although the current position is stated to have an elevation a, it does not
   change the result)
 - any heights from a to z have a value respectively from 1 to 26
 - the end position has a value of 0 (same as current position, although it is assumed to have an elevation z)

The heightmap is to put in a numpy array with the numerical values mentioned above.
We use the Dijkstra's algorithm in both parts but in different ways

For port 1:
We build a graph, by parsing all positions from the numpy array. For every position, we add a new node on the
graph, and then look at the neighbour positions up, down, left, and right, and set a vertex for every position that
has a height from 1 up to at most one higher than the current position.
We run the Dijkstra's algorithm with this graph from the current position, and just return the distance to the
end position.

For port 2:
We proceed in the same way, but instead we look at the neighbour positions in a descending way. That is, we set
a vertex for every position that has a height at least one lower than the current position.
We run the Dijkstra's algorithm with this graph from the end position, and return the shortest distance found from
all positions which has a height a (or 1 numerically).

"""

import sys
import numpy as np


def chr2level(ch):
    # Convert each height letter to a numerical value, like mentioned above.
    if ch == 'S':
        return 0
    elif ch == 'E':
        return 27
    else:
        return ord(ch) - ord('a') + 1


def dijkstra(graph, start):
    # The Dijkstra's algorithm

    # Initialize
    Q = set(graph.keys())
    dist = {node: float('infinity') for node in Q}
    dist[start] = 0

    while Q:
        # Select closest node
        u = min(Q, key=lambda node: dist[node])
        Q.remove(u)

        # Update distances of neighbour nodes
        for v in graph[u]:
            if dist[v] > dist[u] + 1:
                dist[v] = dist[u] + 1

    return dist


def find_best_distance_to_end(grid, start, end):
    # Initialize a dict graph
    graph = {}

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            # Always create a new node for each position
            graph[(x, y)] = []
            for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                # The neighbor positions must be i the boundary of the array
                if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]:
                    # Set a vertex for every position that has a height from 1 up to at most one higher than
                    # the current position.
                    if 1 <= grid[neighbor[0]][neighbor[1]] <= grid[x, y] + 1:
                        graph[(x, y)].append((neighbor[0], neighbor[1]))

    # Run the Dijkstra's algorithm from the current position and return the distance to the end position.
    dist = dijkstra(graph, start)
    return dist[end]


def get_best_distance_from_a(grid, end):
    # Initialize a dict graph
    graph = {}

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            # Always create a new node for each position
            # To keep track of the height on the nodes, we also add the height in the node name. This will be useful
            # later to find the best distance
            graph[(x, y, grid[x, y])] = []
            for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                # The neighbor positions must be i the boundary of the array
                if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]:
                    # Set a vertex for every position that has a height at least one lower than the current position
                    if grid[neighbor[0]][neighbor[1]] >= grid[x, y] - 1:
                        graph[(x, y, grid[x, y])].append((neighbor[0], neighbor[1], grid[neighbor[0], neighbor[1]]))

    # Run the Dijkstra's algorithm from the end position and return the shortest distance found from
    # all positions which has a height a
    dist = dijkstra(graph, end)
    return min([dist[d] for d in dist if d[2] == chr2level('a')])


def parse_heightmap(file):
    # First parse to find the size of the heightmap
    with open(file) as f:
        size_x, size_y = 0, 0

        for line in f:
            size_x = max(size_x, len(line.rstrip()))
            size_y += 1

    # Initialize the array
    grid = np.ndarray((size_x, size_y), dtype=int)
    start_coord = None
    end_coord = None

    # Second parse to fill the array
    with open(file) as f:
        y = 0
        for line in f:
            line = line.rstrip()
            grid[:, y] = [chr2level(x) for x in line]

            # Note the current and end position
            if line.find("S") >= 0:
                start_coord = (line.find('S'), y)
            if line.find("E") >= 0:
                end_coord = (line.find('E'), y)
            y += 1

    return grid, start_coord, end_coord


def display_heightmap(grid):
    # Display the heightmap (for debugging purpose only)
    for y in range(grid.shape[1]):
        print(" ".join([f"{grid[x, y]:02}" for x in range(grid.shape[0])]))


def day12_1(file):
    grid, start_coord, end_coord = parse_heightmap(file)
    print(find_best_distance_to_end(grid, start_coord, end_coord))


def day12_2(file):
    grid, start_coord, end_coord = parse_heightmap(file)
    # We keep track of the height on the nodes
    end_coord = (end_coord[0], end_coord[1], chr2level('E'))
    print(get_best_distance_from_a(grid, end_coord))


if __name__ == '__main__':
    day12_1(sys.argv[1])
    day12_2(sys.argv[1])

