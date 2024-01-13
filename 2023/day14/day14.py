#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/14
#

import sys
import numpy as np
import hashlib

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

    return grid


def tilt_grid(grid, rotate=0):
    # Rotate the grid to change to the tilt direction
    # 0: north, 1: west, 2: south, 3: east
    grid = np.rot90(grid, k=rotate)

    # Initialize a new grid array with the same shape as the existing grid.
    new_grid = np.copy(grid)

    while True:
        # Initialize a counter to keep track of the number of tilts
        nb_tilt = 0

        # Nested loops to iterate through each cell in the grid.
        for y in range(grid.shape[1]):
            for x in range(grid.shape[0]):
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

    # Rotate the grid back to its original orientation
    grid = np.rot90(grid, k=(-rotate) % 4)

    # Return the final configuration of the grid after all iterations.
    return grid


def tilt_cycle_grid(grid):
    # Fopr part 2, the number of iterations is very huge.
    # Our hypothesis is that there exists a cycle starting at a certain point. To detect this cycle, we compute
    # a footprint hash at each cycle, store it, and then compare it with those who as been already. If we find a
    # footprint hash that has already been computed, then we have completed a cycle.
    # Guessing the final value is then very straightforward, with a bit of math and modulo arithmetic.

    # Initialize an empty dictionary to store the hashes.
    hashes = {}

    # Initialize an empty list to store total loads for each unique grid configuration.
    # This will be useful in the final step to guess the result
    total_loads = []

    # Initialize flags and variables related to hash cycles.
    hash_cycle = False
    hash_cycle_start = 0

    # Iterate up to 1 billion times (1_000_000_000).
    for n in range(1_000_000_000):
        # Rotate the grid four times using the 'tilt_grid' function with different direction:
        # north, then west, then south, then east
        for k in range(4):
            grid = tilt_grid(grid, rotate=k)

        # Convert the grid's data to bytes and compute its SHA-1 hash.
        hash_grid = hashlib.sha1(grid.data.tobytes()).hexdigest()

        # Check if the hash of the grid is not already in the hashes dictionary.
        if hash_grid not in hashes:
            # If the hash is new, store it in the hashes dictionary with its corresponding index.
            hashes[hash_grid] = n
            # Calculate and append the total load of the current grid configuration to the list.
            total_loads.append(find_total_load(grid))
        else:
            # If the hash is already present in 'hashes', it indicates a cycle.
            # Calculate the length of the cycle and the starting iteration of the cycle.
            hash_cycle = n - hashes[hash_grid]
            hash_cycle_start = hashes[hash_grid]
            # Break out of the loop since a cycle has been detected.
            break

    # Compute the index of the total load to return based on the hash cycle.
    # This is done by calculating the appropriate index in the 'total_loads' list using modulo arithmetic.
    return total_loads[(1_000_000_000 - hash_cycle_start) % hash_cycle + hash_cycle_start - 1]


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
    grid = parse_grid(file)
    print(tilt_cycle_grid(grid))


if __name__ == '__main__':
    day14_1(sys.argv[1])
    day14_2(sys.argv[1])

