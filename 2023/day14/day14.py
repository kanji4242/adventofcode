#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/14
#

import sys
import numpy as np

GRID_ROUNDED_ROCK = "O"
GRID_CUBED_ROCK = "#"
GRID_EMPTY = "."


def display_grid(grid):
    # For debugging purpose, display the grid array
    for y in range(grid.shape[1]):
        print(''.join([grid[x, y] for x in range(grid.shape[0])]))


def parse_grid(file):
    with open(file) as f:
        size_x, size_y = 0, 0

        for line in f:
            size_x = max(size_x, len(line.rstrip()))
            size_y += 1

        # Initialize the array
        grid = np.ndarray((size_x, size_y), dtype=object)

    # Second parse to fill the array
    with open(file) as f:
        y = 0
        for line in f:
            grid[:, y] = [ch for ch in line.rstrip()]
            y += 1

    display_grid(grid)
    return grid


def tilt_grid(grid):
    while True:
        # Initialize a new grid array with the same shape as the existing grid.
        new_grid = np.ndarray(grid.shape, dtype=object)

        # Initialize a counter to keep track of the number of tilts
        nb_tilt = 0

        # Nested loops to iterate through each cell in the grid.
        for y in range(grid.shape[1]):
            for x in range(grid.shape[0]):
                # Copy the value from the current cell in the original grid to the new grid.
                new_grid[x, y] = grid[x, y]

                # Check conditions to see if a cell is a rounded rock
                if y > 0 and grid[x, y] == GRID_ROUNDED_ROCK:
                    if grid[x, y] == GRID_ROUNDED_ROCK:
                        # If the current cell contains a rounded rock and the cell above it is empty,
                        # then update the positions in the new grid and increment the tilt counter.
                        if grid[x, y - 1] == GRID_EMPTY:
                            new_grid[x, y - 1] = GRID_ROUNDED_ROCK
                            new_grid[x, y] = GRID_EMPTY
                            nb_tilt += 1

        # Update the original grid with the new grid configuration.
        grid[:, :] = new_grid[:, :]

        # If no tiles were tilted in this iteration, break out of the loop.
        if nb_tilt == 0:
            break

    # Return the final configuration of the grid after all iterations.
    return new_grid


def find_total_load(grid):
    total_load = 0

    # Nested loops to iterate through each cell in the grid.
    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):

            # Check if the current cell contains a rounded rock.
            if grid[x, y] == GRID_ROUNDED_ROCK:
                # If a rounded rock is found at this position, calculate its load based on its position.
                # The load is determined by the number of rows from the rock to the south edge.
                # This is achieved by subtracting the current y-coordinate from the total number
                # of rows (grid.shape[1]).
                load_for_current_rock = grid.shape[1] - y

                # Add the load of the current rounded rock to the total load.
                total_load += load_for_current_rock

    # Return the computed total load.
    return total_load


def day14_1(file):
    grid = parse_grid(file)
    print(find_total_load(tilt_grid(grid)))


def day14_2(file):
    print(parse_grid(file))


if __name__ == '__main__':
    day14_1(sys.argv[1])
    #day14_2(sys.argv[1])

