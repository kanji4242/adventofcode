#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2024/day/4
#

import sys
import numpy as np
import re


def parse_grid(file):
    with open(file) as f:
        size_x, size_y = 0, 0

        for line in f:
            size_x = max(size_x, len(line.rstrip()))
            size_y += 1

        # Initialize the array
        grid = np.ndarray((size_x, size_y), dtype=int)

    # Second parse to fill the array
    with open(file) as f:
        y = 0
        for line in f:
            grid[:, y] = [ord(ch) for ch in line.rstrip()]
            y += 1

    return grid


def get_nb_xmas_in_line(line):
    return len([m.group() for m in re.finditer("XMAS", line)])


def find_xmas(grid):
    nb_xmas = 0

    # Parse lines
    for y in range(grid.shape[1]):
        string = ''.join([chr(ch) for ch in grid[:, y]])
        nb_xmas += get_nb_xmas_in_line(string)
        nb_xmas += get_nb_xmas_in_line(string[::-1])

    # Parse columns
    for x in range(grid.shape[0]):
        string = ''.join([chr(ch) for ch in grid[x, :]])
        nb_xmas += get_nb_xmas_in_line(string)
        nb_xmas += get_nb_xmas_in_line(string[::-1])

    # Parse diagonals
    for y in range(1 - grid.shape[1], grid.shape[1] - 1):
        string = ''.join([chr(ch) for ch in grid.diagonal(y)])
        nb_xmas += get_nb_xmas_in_line(string)
        nb_xmas += get_nb_xmas_in_line(string[::-1])

    flipped_grid = np.flip(grid, 0)

    # Parse reverse diagonals
    for x in range(1 - grid.shape[0], grid.shape[0] - 1):
        string = ''.join([chr(ch) for ch in flipped_grid.diagonal(x)])
        nb_xmas += get_nb_xmas_in_line(string)
        nb_xmas += get_nb_xmas_in_line(string[::-1])

    print(nb_xmas)


def find_xmas_x_shaped(grid):
    nb_xmas = 0

    # Loop through all grid cells except the edges (to prevent out-of-bounds access)
    # Iterate over columns
    for y in range(1, grid.shape[1] - 1):
        # Iterate over rows
        for x in range(1, grid.shape[0] - 1):

            # Check if the current cell contains the character 'A'
            if chr(grid[x, y]) == 'A':
                # Extract a 3x3 sub-grid centered on the current cell
                sub_grid = grid[x - 1:x + 2, y - 1:y + 2]

                # Check all 4 rotations of the sub-grid for a matching pattern
                for n in range(4):
                    # Rotate the sub-grid 90 degrees clockwise
                    sub_grid = np.rot90(sub_grid)

                    # Check for the XMAS pattern: 'M' in top corners, 'S' in bottom corners
                    if sub_grid[0, 0] == ord('M') and sub_grid[0, 2] == ord('M') \
                            and sub_grid[2, 0] == ord('S') and sub_grid[2, 2] == ord('S'):
                        # Increment counter if the pattern is found and stop further rotations, as pattern
                        # is already matched
                        nb_xmas += 1
                        break

                    # Check for the inverted XMAS pattern: 'S' in top corners, 'M' in bottom corners
                    elif sub_grid[0, 0] == ord('S') and sub_grid[0, 2] == ord('S') \
                            and sub_grid[2, 0] == ord('M') and sub_grid[2, 2] == ord('M'):
                        # Increment counter if the pattern is found and stop further rotations, as pattern
                        # is already matched
                        nb_xmas += 1
                        break

    print(nb_xmas)


def day4_1(file):
    grid = parse_grid(file)
    find_xmas(grid)


def day4_2(file):
    grid = parse_grid(file)
    find_xmas_x_shaped(grid)


if __name__ == '__main__':
    day4_1(sys.argv[1])
    day4_2(sys.argv[1])
