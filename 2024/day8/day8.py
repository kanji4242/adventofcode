#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2024/day/8
#

import sys
import numpy as np


def display_grid(grid):
    # For debugging purpose, display the grid array
    for y in range(grid.shape[1]):
        cells = [f"{grid[x, y]:2}" for x in range(grid.shape[0])]
        print(' '.join(cells))


def parse_grid(file):
    antennas_list = {}

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
            line = line.rstrip()
            for x in range(len(line)):
                if line[x] == '.':
                    grid[x, y] = 0
                else:
                    grid[x, y] = ord(line[x])
                    if ord(line[x]) not in antennas_list:
                        antennas_list[ord(line[x])] = [(x, y)]
                    else:
                        antennas_list[ord(line[x])].append((x, y))
            y += 1

    return grid, antennas_list


def find_antinodes(grid, antennas_list):
    nb_antinodes = 0
    # The antinodes found will be noted on a separate grid, in order to be sure not counting them twice
    antinodes_grid = np.zeros(grid.shape, dtype=int)

    for freq, antennas in antennas_list.items():
        # Get all couples of antennas with the same frequency.
        for coord_a, coord_b in [(a, b) for idx, a in enumerate(antennas) for b in antennas[idx + 1:]]:
            # Examine the 2 possible locations for the antinodes
            for coord_antinode in [(2 * coord_b[0] - coord_a[0], 2 * coord_b[1] - coord_a[1]),
                                   (2 * coord_a[0] - coord_b[0], 2 * coord_a[1] - coord_b[1])]:
                # If the location is within the grid boundaries and there is no antinode, add it
                if 0 <= coord_antinode[0] < grid.shape[0] and 0 <= coord_antinode[1] < grid.shape[1]\
                        and antinodes_grid[coord_antinode] == 0:
                    antinodes_grid[coord_antinode] = 1
                    nb_antinodes += 1

    return nb_antinodes


def find_antinodes2(grid, antennas_list):
    nb_antinodes = 0
    # The antinodes found will be noted on a separate grid, in order to be sure not counting them twice
    antinodes_grid = np.zeros(grid.shape, dtype=int)

    for freq, antennas in antennas_list.items():
        # Get all couples of antennas with the same frequency.
        for coord_a, coord_b in [(a, b) for idx, a in enumerate(antennas) for b in antennas[idx + 1:]]:
            distance = (coord_b[0] - coord_a[0], coord_b[1] - coord_a[1])

            # Examine the possible locations iteratively looking upward
            antinodes_candidate = (coord_a[0], coord_a[1])
            # We stop if we get outside the boundaries of the grid
            while 0 <= antinodes_candidate[0] < grid.shape[0] and 0 <= antinodes_candidate[1] < grid.shape[1]:
                # If there is no antinode on this location, add it
                if antinodes_grid[antinodes_candidate] == 0:
                    antinodes_grid[antinodes_candidate] = 1
                    nb_antinodes += 1
                # Go forward to the next location upward
                antinodes_candidate = (antinodes_candidate[0] - distance[0], antinodes_candidate[1] - distance[1])

            # Examine the possible locations iteratively looking downward
            antinodes_candidate = (coord_b[0], coord_b[1])
            # We stop if we get outside the boundaries of the grid
            while 0 <= antinodes_candidate[0] < grid.shape[0] and 0 <= antinodes_candidate[1] < grid.shape[1]:
                # If there is no antinode on this location, add it
                if antinodes_grid[antinodes_candidate] == 0:
                    antinodes_grid[antinodes_candidate] = 1
                    nb_antinodes += 1
                # Go forward to the next location downward
                antinodes_candidate = (antinodes_candidate[0] + distance[0], antinodes_candidate[1] + distance[1])

    return nb_antinodes


def day8_1(file):
    grid, antennas_list = parse_grid(file)
    print(find_antinodes(grid, antennas_list))


def day8_2(file):
    grid, antennas_list = parse_grid(file)
    print(find_antinodes2(grid, antennas_list))


if __name__ == '__main__':
    day8_1(sys.argv[1])
    day8_2(sys.argv[1])
