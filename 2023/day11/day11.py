#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/11
#

import sys
import numpy as np
from itertools import combinations

SPACE_EMPTY = 0
SPACE_GALAXY = 1

SPACE = {
    '.': SPACE_EMPTY,
    '#': SPACE_GALAXY
}


def manhattan_distance(coord1, coord2):
    # Calculate the Manhattan distance between two coordinates coord1 (x1, y1) and coord2 (x2, y2).
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def display_galaxy(space):
    # For debugging purpose, display the space array
    inverted_space = {v: k for k, v in SPACE.items()}

    for y in range(space.shape[1]):
        print(''.join([inverted_space[space[x, y]] for x in range(space.shape[0])]))


def expand_coord(cols_empty, rows_empty, coord, expansion=1):
    """
    Expand the given coordinates based on the columns and rows that are empty.

    Parameters:
    - cols_empty: List containing indices of empty columns in the space.
    - rows_empty: List containing indices of empty rows in the space.
    - coord: Tuple containing the original coordinates (x, y) to be expanded.
    - expansion: Value by which the coordinates should be expanded.

    Returns:
    - Tuple containing the expanded coordinates (new_x, new_y).
    """

    # Initialize new coordinates to the original coordinates.
    new_coord_x = coord[0]
    new_coord_y = coord[1]

    # Iterate over the indices of empty columns
    for n in range(len(cols_empty)):
        # If the x-coordinate of the original point is greater than the index of an empty column,
        # adjust the new x-coordinate by adding the expansion value
        if coord[0] > cols_empty[n]:
            new_coord_x = coord[0] + (n + 1) * expansion

    # Iterate over the indices of empty rows
    for n in range(len(rows_empty)):
        # If the y-coordinate of the original point is greater than the index of an empty row,
        # adjust the new y-coordinate by adding the expansion value
        if coord[1] > rows_empty[n]:
            new_coord_y = coord[1] + (n + 1) * expansion

    # Create a tuple with the new x and y coordinates and return it
    result = (new_coord_x, new_coord_y)
    return result


def parse_file(file):
    with open(file) as f:
        size_x, size_y = 0, 0

        for line in f:
            size_x = max(size_x, len(line.rstrip()))
            size_y += 1

        # Initialize the array
        space = np.ndarray((size_x, size_y), dtype=int)

    # Second parse to fill the array
    with open(file) as f:
        y = 0
        for line in f:
            space[:, y] = [SPACE[ch] for ch in line.rstrip()]
            y += 1

    #display_galaxy(space)
    return space


def find_shortest_paths(space, expansion=2):
    # Initialize empty lists to store information about galaxies, columns, and rows that are empty.
    galaxies = []
    columns_empty = []
    rows_empty = []

    # Determine the shape (dimensions) of the space array.
    size_x, size_y = space.shape

    # Check each column in space for empty galaxies (where SPACE_GALAXY is not present).
    for x in range(size_x):
        if np.count_nonzero(space[x, :] == SPACE_GALAXY) == 0:
            columns_empty.append(x)

    # Check each row in space for empty galaxies.
    for y in range(size_y):
        if np.count_nonzero(space[:, y] == SPACE_GALAXY) == 0:
            rows_empty.append(y)

    # Traverse each cell in space to identify and process galaxies.
    for y in range(size_y):
        for x in range(size_x):
            # If a cell contains a galaxy (i.e., has the value SPACE_GALAXY),
            # expand its coordinates and store them in the 'galaxies' list.
            if space[x, y] == SPACE_GALAXY:
                galaxies.append(expand_coord(columns_empty, rows_empty, (x, y), expansion - 1))

    # Compute the Manhattan distance between all pairs of galaxies in the 'galaxies' list
    # This involves generating combinations of galaxies and summing up their Manhattan distances
    # We use combinations function from the itertools module
    return sum([manhattan_distance(p[0], p[1]) for p in list(combinations(galaxies, 2))])


def day11_1(file):
    space = parse_file(file)
    print(find_shortest_paths(space))


def day11_2(file):
    space = parse_file(file)
    print(find_shortest_paths(space, expansion=1_000_000))


if __name__ == '__main__':
    day11_1(sys.argv[1])
    day11_2(sys.argv[1])

