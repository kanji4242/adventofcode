#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/17
#

import sys
import numpy as np


class Rock:
    def __init__(self, cells):
        self.cells = cells
        self.shape = (max([c[0] for c in cells]) + 1, max([c[1] for c in cells]) + 1)


class Chamber:
    CELL_VOID = 0
    CELL_FROZEN_ROCK = 1
    CELL_FALLING_ROCK = 2
    CHAMBER_SYMBOLS = ['.', '#', '@']

    def __init__(self):
        self._init_grid()
        # Max height is set to 1 because we will add bedrock layer (at y=0)
        self.max_height = 1
        self.rock = None
        self.rock_coords = None

    def _init_grid(self):
        # Init grid and fill it with void
        self.grid = np.ndarray((7, 5000), dtype=int)
        self.grid.fill(self.CELL_VOID)

        # Fill the ground (y=0) with frozen rock to ease the falling algorithm
        # This explains why the max height is set to 1
        for x in range(self.grid.shape[0]):
            self.grid[x][0] = self.CELL_FROZEN_ROCK

    def add_rock(self, rock):
        # Add new rock set its coordinates three units above the highest rock
        self.rock = rock
        self.rock_coords = [2, self.max_height + 3]

    def blow_and_fall_rock(self, direction, jet_patterns_index):
        # Convert the direction symbol (< or >) to "vector" direction
        direction = -1 if direction == "<" else 1

        # Push the rock pushed by a jet
        can_move = True
        for c in self.rock.cells:
            new_x = self.rock_coords[0] + c[0] + direction
            # The rock cannot move into the walls, floor, or a frozen rock
            if new_x < 0 or new_x >= self.grid.shape[0]\
                    or self.grid[new_x][self.rock_coords[1] + c[1]] == self.CELL_FROZEN_ROCK:
                can_move = False
                break

        # If the rock can move, update the rock coordinates according to the jet direction
        if can_move:
            self.rock_coords[0] = self.rock_coords[0] + direction

        # Try to fall the rock
        can_fall = True
        for c in self.rock.cells:
            # Space behind the rock must be void
            if self.grid[self.rock_coords[0] + c[0]][self.rock_coords[1] + c[1] - 1] == self.CELL_FROZEN_ROCK:
                can_fall = False
                break

        # If the rock can fall, update the rock coordinates down to 1
        if can_fall:
            self.rock_coords[1] = self.rock_coords[1] - 1

        return can_fall

    def freeze_rock(self):
        # Freeze a falling rock when it cannot move downward
        for c in self.rock.cells:
            new_x = self.rock_coords[0] + c[0]
            new_y = self.rock_coords[1] + c[1]
            self.grid[new_x][new_y] = self.CELL_FROZEN_ROCK

        # Update the max height depending on where the rock has been frozen
        if self.rock_coords[1] > self.max_height:
            self.max_height += self.rock_coords[1]
        else:
            self.max_height = max(self.max_height, self.rock_coords[1] + self.rock.shape[1])

        self.rock_coords = None
        self.rock = None

    def display_chamber(self, max_y=25):
        # Display grid (for debugging purpose only)
        display_grid = self.grid.copy()

        if self.rock:
            for c in self.rock.cells:
                display_grid[self.rock_coords[0] + c[0]][self.rock_coords[1] + c[1]] = self.CELL_FALLING_ROCK
        for y in range(max_y - 1, -1, -1):
            print("|" + "".join([self.CHAMBER_SYMBOLS[display_grid[x][y]]
                                 for x in range(display_grid.shape[0])]) + "|")

        print("max height:", self.max_height - 1)
        print("")


def init_rocks():
    # Initialize all rock type
    return [
        Rock([(0, 0), (1, 0), (2, 0), (3, 0)]),
        Rock([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]),
        Rock([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
        Rock([(0, 0), (0, 1), (0, 2), (0, 3)]),
        Rock([(0, 0), (1, 0), (0, 1), (1, 1)]),
    ]


def day17_1(file):
    with open(file) as f:
        jet_patterns = list(f.readline().strip())

    jet_patterns_index = 0
    rock_index = 0

    rocks = init_rocks()
    chamber = Chamber()

    while rock_index < 2022:
        chamber.add_rock(rocks[rock_index % len(rocks)])
        #chamber.display_chamber()

        while chamber.blow_and_fall_rock(jet_patterns[jet_patterns_index], jet_patterns_index):
            jet_patterns_index = (jet_patterns_index + 1) % len(jet_patterns)
            #chamber.display_chamber()

        jet_patterns_index = (jet_patterns_index + 1) % len(jet_patterns)
        chamber.freeze_rock()
        #chamber.display_chamber()

        rock_index += 1

    # Print max height minus 1 because we had a bedrock layer added
    print(chamber.max_height - 1)


def day17_2(file):
    pass


if __name__ == '__main__':
    day17_1(sys.argv[1])
    #day17_2(sys.argv[1])
