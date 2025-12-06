#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2025/day/4
#

import sys
import numpy as np

mapping = { '.': 0, '@': 1, 'x': 2 }

def display_grid(grid):
    reverse_mapping = {v: k for k,v in mapping.items()}
    # For debugging purpose, display the grid array
    for y in range(grid.shape[1]):
        print(''.join([reverse_mapping[grid[x, y]] for x in range(grid.shape[0])]))


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
            grid[:, y] = [mapping[ch] for ch in line.rstrip()]
            y += 1

    return grid

def roll_can_removed(grid, x, y):
    grid_adjacent = grid[max(0, x - 1):min(x + 2, grid.shape[0]), max(0, y - 1):min(y + 2, grid.shape[1])]
    return np.count_nonzero(grid_adjacent == 1) <= 4

def get_nb_rolls(grid):
    nb_rolls = 0

    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            if grid[x, y] == 1 and roll_can_removed(grid, x, y):
                nb_rolls += 1

    return nb_rolls

def get_nb_rolls_removed(grid):
    current_grid = np.copy(grid)
    new_grid = np.copy(grid)
    nb_rolls_removed = 0

    while True:
        rolls_removed = False
        for y in range(grid.shape[1]):
            for x in range(grid.shape[0]):
                if current_grid[x, y] == 1 and roll_can_removed(current_grid, x, y):
                    nb_rolls_removed += 1
                    new_grid[x, y] = 0
                    rolls_removed = True

        current_grid = np.copy(new_grid)
        new_grid = np.copy(new_grid)
        if not rolls_removed:
            break

    return nb_rolls_removed

def day4_1(file):
    print(get_nb_rolls(parse_grid(file)))

def day4_2(file):
    print(get_nb_rolls_removed(parse_grid(file)))


if __name__ == '__main__':
    day4_1(sys.argv[1])
    day4_2(sys.argv[1])

