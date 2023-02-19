#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/18
#

import sys
import numpy as np
from queue import Queue

CELL_AIR = 0
CELL_LAVA = 1
CELL_EXT_AIR = 4


def display_slice(grid):
    # Display slices from Z-axis (for debugging purpose only)
    symbols = {CELL_AIR: ".", CELL_LAVA: "#", CELL_EXT_AIR: "+"}

    for y in range(grid.shape[1]):
        print("".join([symbols[grid[x][y]] for x in range(grid.shape[0])]))


def fill_exterior(grid):
    # Only for part2, mark cell filled by air and mark them as exterior air (CELL_EXT_AIR value)
    queue = Queue()

    # We process each cell recursively, but we use the queue method to avoid a stack overflow
    # Start at cell [0, 0, 0] which won't be a lava cell (thanks the air "shell" added)
    queue.put((0, 0, 0))

    # Get a cell until the queue is exhausted
    while not queue.empty():
        coord = queue.get()

        # If this cell is an air cell, mark it as exterior air
        if grid[coord[0]][coord[1]][coord[2]] == CELL_AIR:
            grid[coord[0]][coord[1]][coord[2]] = CELL_EXT_AIR

            # Add all neighbor cells to the queue in all 3 axis (up, down, front, back, left, right)
            if coord[0] + 1 < grid.shape[0]:
                queue.put((coord[0] + 1, coord[1], coord[2]))
            if coord[0] - 1 < grid.shape[0]:
                queue.put((coord[0] - 1, coord[1], coord[2]))

            if coord[1] + 1 < grid.shape[1]:
                queue.put((coord[0], coord[1] + 1, coord[2]))
            if coord[1] - 1 < grid.shape[1]:
                queue.put((coord[0], coord[1] - 1, coord[2]))

            if coord[2] + 1 < grid.shape[2]:
                queue.put((coord[0], coord[1], coord[2] + 1))
            if coord[2] - 1 < grid.shape[2]:
                queue.put((coord[0], coord[1], coord[2] - 1))


def parse_coords(file):
    # Parse cubes coordinates from file and insert in a list of tuples
    with open(file) as f:
        coords = []
        for line in f:
            coord_x, coord_y, coord_z = [int(x) for x in line.strip().split(',')]
            coords.append((coord_x, coord_y, coord_z))

        # Prepare a grid from this list, but before, find the max values (there are no negative values) for the 3
        # dimensions and add 4 in order to enclose the lava droplet into an air "shell". This simplifies the surface
        # area algorithm by avoid special cases related to the border and index in the grid. This "shell" also
        # ensure that the cell at [0, 0, 0] won't be a lava cell which will be important for fill algorithm used
        # in part2.
        max_x, max_y, max_z = max([c[0] for c in coords]) + 4, \
                               max([c[1] for c in coords]) + 4, \
                               max([c[2] for c in coords]) + 4

    # Create the grid and fill it with air
    grid = np.ndarray((max_x, max_y, max_z), dtype=int)
    grid.fill(CELL_AIR)

    # Insert the droplet coordinates
    for coord in coords:
        # We add 2 to the coordinates for the air "shell"
        grid[coord[0] + 2][coord[1] + 2][coord[2] + 2] = CELL_LAVA

    return grid


def find_surface_area(grid, value):
    surface = 0

    # We consider every 2 consecutive slices (2 2x2 matrices) for each axis X, Y and Z and subtract them.
    # An exposed face imply 2 adjacent cells, one with air and the other with lava, or the reverse
    # In terms of numeric value, their difference will be equal to CELL_AIR - CELL_LAVA
    # or CELL_LAVA - CELL_AIR, other difference value won't be considered and won't be counted for
    # the surface area.
    # We can use the absolute value to handle both cases at the same time
    # For part2, CELL_EXT_AIR will be considered instead of CELL_AIR
    # Note that CELL_AIR, CELL_EXT_AIR and CELL_LAVA numeric values have been well-chosen to have a unique
    # value when computing their difference
    for x in range(grid.shape[0]):
        surface += np.count_nonzero(np.absolute(grid[x, :, :] - grid[x - 1, :, :]) == value)
    for y in range(grid.shape[1]):
        surface += np.count_nonzero(np.absolute(grid[:, y, :] - grid[:, y - 1, :]) == value)
    for z in range(grid.shape[2]):
        surface += np.count_nonzero(np.absolute(grid[:, :, z] - grid[:, :, z - 1]) == value)

    return surface


def day18_1(file):
    lava_grid = parse_coords(file)
    print(find_surface_area(lava_grid, abs(CELL_AIR - CELL_LAVA)))


def day18_2(file):
    lava_grid = parse_coords(file)
    fill_exterior(lava_grid)
    print(find_surface_area(lava_grid, abs(CELL_EXT_AIR - CELL_LAVA)))


if __name__ == '__main__':
    day18_1(sys.argv[1])
    day18_2(sys.argv[1])
