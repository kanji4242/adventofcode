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
    CELL_MARK = 3

    # For display_chamber method only
    CHAMBER_SYMBOLS = ['.', '#', '@', '+']

    def __init__(self, rocks, jet_patterns, max_rocks):
        # Max height is set to 1 because we will add a bedrock layer at y=0
        self.jet_patterns = jet_patterns
        self.rocks = rocks
        self.max_rocks = max_rocks

        self._init_grid()
        self.max_height = 1

        self.rock = None
        self.rock_coords = None

    def _init_grid(self):
        # Init grid and fill it with void
        self.grid = np.ndarray((7, 50000), dtype=int)
        self.grid.fill(self.CELL_VOID)

        # Fill the ground (at y=0) with a bedrock of frozen rock to help the falling algorithm
        # This explains why the max height is set to 1
        for x in range(self.grid.shape[0]):
            self.grid[x][0] = self.CELL_FROZEN_ROCK

    def add_rock(self, rock):
        # Add new rock and set its coordinates two units away from the left and three units above the highest rock
        self.rock = rock
        self.rock_coords = [2, self.max_height + 3]

    def blow_and_fall_rock(self, direction):
        # Move the rock according to jet and try to fall it down
        # Convert the jet direction symbol (< or >) to "vector" direction
        direction = -1 if direction == "<" else 1

        # Push the rock by the jet direction
        can_move = True
        for c in self.rock.cells:
            new_x = self.rock_coords[0] + c[0] + direction
            # The rock cannot move through the walls, floor, or a frozen rock
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
            if self.grid[self.rock_coords[0] + c[0]][self.rock_coords[1] + c[1] - 1]\
                    == self.CELL_FROZEN_ROCK:
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

        # Update the max height depending on where the rock has fallen
        if self.rock_coords[1] > self.max_height:
            self.max_height += self.rock_coords[1]
        else:
            self.max_height = max(self.max_height, self.rock_coords[1] + self.rock.shape[1])

        # The rock has been treated, so empty its datas
        self.rock_coords = None
        self.rock = None

    def display_chamber(self, lines=25):
        # Display grid (for debugging purpose only)
        display_grid = self.grid.copy()

        if self.rock:
            for c in self.rock.cells:
                display_grid[self.rock_coords[0] + c[0]][self.rock_coords[1] + c[1]]\
                    = self.CELL_FALLING_ROCK

        for y in range(min(self.max_height + 2, display_grid.shape[1]),
                       max(-1, self.max_height - lines + 2), -1):
            print("|" + "".join([self.CHAMBER_SYMBOLS[display_grid[x][y]]
                                 for x in range(display_grid.shape[0])]) + "| " + str(y))

        print("max height:", self.max_height - 1)
        print("")

    def run(self, part2=False):
        # Incrementation index to rotate over rocks and jet patterns
        rock_index = 0
        jet_patterns_index = 0

        # For part2 (explained below)
        max_height = 1
        max_heights_pattern = []
        record_pattern = False
        initial_height = 0
        initial_rock = 0

        while rock_index < self.max_rocks or part2:
            # We add new rock
            self.add_rock(self.rocks[rock_index % len(self.rocks)])

            # If the rock can fall, we continue to do so
            while self.blow_and_fall_rock(self.jet_patterns[jet_patterns_index % len(self.jet_patterns)]):
                jet_patterns_index += 1

            # The rock cannot fall anymore, we freeze it
            self.freeze_rock()

            if part2:
                # The part2 is trickier, the idea is the following:
                #  - Simulating the result of one trillion rocks using the first method is impossible as it would
                #    insanely take too much time (more than one year of calculation), we have to be clever ...
                #  - Since we're rotating over rocks and jet patterns, their indexes vary from O to the number of
                #    elements - 1. When inspecting these indexes for each iteration we can notice a recurring cycle
                #    between their respective indexes. The experiments I did show that when the jet patterns index
                #    reach 0 we've achieved a cycle. When this event occurs, we note how many rocks has fallen and
                #    how many jet patterns we consumed.
                #  - We also need to store the height delta for every step of this cycle (because 1 step also means
                #    a new rock added). And we also need to note the current height and rocks counters when the
                #    1st cycle occurs.
                #  - Once we have this information, we can calculate the result using a simple formula involving
                #    division and modulo and the information above
                if record_pattern:
                    # If we are within the cycle, we record the height delta in a list
                    max_heights_pattern.append(self.max_height - max_height)

                if jet_patterns_index % len(self.jet_patterns) == 0 and not len(max_heights_pattern):
                    # The 1st cycle starts
                    # We note the current height and rocks counters
                    initial_height = self.max_height
                    initial_rock = rock_index

                    # We activate the recording of height delta at every step
                    record_pattern = True
                    max_height = self.max_height

                elif jet_patterns_index % len(self.jet_patterns) == 0 and len(max_heights_pattern):
                    # We reached the end of the cycle, we stop iterating as we have all information
                    break

                if jet_patterns_index % len(self.jet_patterns) == 0:
                    # We store the previous height to get the height delta
                    max_height = self.max_height

            rock_index += 1
            jet_patterns_index += 1

        # In both case, returns the height minus 1 because we added a bedrock layer
        if part2:
            # Calculate the quotient which we be the number of total cycles
            quotient = int((self.max_rocks - initial_rock + 1) / len(max_heights_pattern))
            # Same for the modulo which the rest for the final height, this delta will be found from the height
            # delta list
            modulo = (self.max_rocks - initial_rock - 2) % len(max_heights_pattern)

            return initial_height + quotient * max_heights_pattern[-1] + max_heights_pattern[modulo] - 1
        else:
            return self.max_height - 1


def init_rocks():
    # Initialize all rock type, each tuples is a rock component coordinate
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

    rocks = init_rocks()
    chamber = Chamber(rocks, jet_patterns, 2022)

    print(chamber.run())
    #chamber.display_chamber(lines=25)


def day17_2(file):
    with open(file) as f:
        jet_patterns = list(f.readline().strip())

    rocks = init_rocks()
    chamber = Chamber(rocks, jet_patterns, 1_000_000_000_000)

    print(chamber.run(part2=True))


if __name__ == '__main__':
    day17_1(sys.argv[1])
    day17_2(sys.argv[1])
