#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/23
#

"""
I had 2 solution ideas:

- parse the input file and build a grid (a numpy array), build a list of elves with their coordinates. And then place
  elves in this grid. According to the rules the elves can extend beyond the grid. To get over this problem, my idea
  is to build significantly larger grid and place the elves on in the center of the grid. By doing this, the elves
  will have room all around to expand. This solution is not super elegant because we don't know how far the elves
  will extend and therefore how much space to add.

- to avoid the problem mentioned above, my 2nd idea is to do without this grid, and to use only the list of elves.
  The advantage of this method is that there is no limit to the coordinates and the elves can expand as much as they
  need. But another problem arises because the rules require a lot of neighbourhood checking, which forces looking up
  the elves list a lot of times to check whether there is an elf or not at the neighbouring coordinates. And these
  list lookups are a big performance issue.

I implemented the 2 solutions, and the second solution is 10x slower than the first one. I opted for the 1st
solution: using a grid with some arbitrary room. To optimize even further I use 2 grids. One of the 2 will be
active, while the other one is inactive and available for the next turn. When the next round comes, this grid become
active while the grid used for the previous turn become inactive. This "round-robin" mechanism allows saving memory
and avoid creating a new grid at each turn.

"""

import sys
import numpy as np


class Grove:
    """
    Grove represents a grove with:
      - the 2 grids (numpy array) where elves will be placed, the first one is active while the second one is inactive,
        as described above.
      - a list of elves
    """
    TILE_GROUND = 0
    TILE_ELF = 1

    TILES = {
        TILE_GROUND: '.',
        TILE_ELF: '#',
    }

    def __init__(self, file):
        self.file = file
        self.grid = None     # The active grid
        self.inactive_grid = None
        self.elves = []

    def parse_grove(self):
        # The extra room we will add to the grid, It indicates how many times the original size of the input file
        # we add the grid in all 4 direction. For instance, a value of 2 will add twice the original size at the top,
        # left, right and bottom, making the grid 5x larger
        extra_shape = 10

        # First parse the input file to get the original size
        with open(self.file) as f:
            size_x, size_y = 0, 0

            for line in f:
                size_x = max(size_x, len(line.rstrip()))
                size_y += 1

        # Build the grid with extra room
        self.grid = np.ndarray((size_x * (2 * extra_shape + 1), size_y * (2 * extra_shape + 1)), dtype=int)
        self.inactive_grid = self.grid.copy()
        tiles_reverse = {v: k for k, v in self.TILES.items()}

        # Parse the input file again and place the elves directly from the line read
        with open(self.file) as f:
            y = 2 * extra_shape
            for line in f:
                line = line.rstrip()
                self.grid[:, y] = [self.TILE_GROUND] * (size_x * extra_shape) + [tiles_reverse[x] for x in line] +\
                                  [self.TILE_GROUND] * (size_x * extra_shape)
                y += 1

        # Parse the grid, lookup where the elves are located and build a list of these elves.
        for y in range(self.grid.shape[1]):
            for x in range(self.grid.shape[0]):
                if self.grid[x, y] == self.TILE_ELF:
                    self.elves.append(Elf(self, Position(x, y)))

    def run(self, max_round=None):
        # Execute the rounds, the max_round parameter set the maximum number of rounds to perform (useful for part 1)
        nb_round = 0
        while True:
            nb_round += 1
            nb_moves = self.do_round()
            if nb_moves == 0 or (max_round is not None and nb_round >= max_round):
                break
            #print(nb_round, nb_moves)

        return nb_round

    def do_round(self):
        # Do a round
        proposed_moves = {}
        nb_moves = 0

        # Let the elves propose a move
        for elf in self.elves:
            elf.propose_move()

        # Go through all the elves and look at their proposed move a build a dict indexed by these proposed coordinates
        # Insert the elves as the value within a list. This method helps identify when 2 elf propose the same
        # coordinates.
        for elf in self.elves:
            proposed_move = tuple(elf.proposed_coord)
            if proposed_move not in proposed_moves:
                proposed_moves[proposed_move] = [elf]
            else:
                proposed_moves[proposed_move].append(elf)

        # Initialize the inactive grid with ground
        self.inactive_grid.fill(self.TILE_GROUND)

        for coord, elves in proposed_moves.items():
            if len(elves) > 1:
                # We have more than 1 elf the list, we have a coordinate collision.
                # So the elves will not move, and we place the elves in their current coordinate in the inactive grid
                for elf in elves:
                    self.inactive_grid[tuple(elf.coord)] = self.TILE_ELF
            else:
                # If we have only 1 elf, that's ok. We place it in the inactive grid according to its proposed
                # new coordinate
                self.inactive_grid[tuple(elves[0].proposed_coord)] = self.TILE_ELF
                if elves[0].coord.x != elves[0].proposed_coord.x or elves[0].coord.y != elves[0].proposed_coord.y:
                    nb_moves += 1

                # We let the elf move to its proposed coordinate
                elves[0].move()

        # The inactive become active
        self.grid, self.inactive_grid = self.inactive_grid, self.grid

        return nb_moves

    def shape(self):
        # Compute the minimum and maximum coordinate where the elves are located on the grid on both axis x and y
        # Useful for displaying the elves in the grid and to calculate the number of ground tiles (part 1)
        min_x, max_x = self.elves[0].coord.x, self.elves[0].coord.x
        min_y, max_y = self.elves[0].coord.y, self.elves[0].coord.y

        for y in range(self.grid.shape[1]):
            for x in range(self.grid.shape[0]):
                if self.grid[x, y] == self.TILE_ELF:
                    min_x, max_x = min(x, min_x), max(x, max_x)
                    min_y, max_y = min(y, min_y), max(y, max_y)

        return min_x, max_x, min_y, max_y

    def get_empty_ground_tiles(self):
        # Compute the number of ground tiles for part 1
        min_x, max_x, min_y, max_y = self.shape()

        return np.count_nonzero(self.grid[min_x:max_x + 1, min_y:max_y + 1] == self.TILE_GROUND)

    def display_grove(self):
        # Display the elves in the grid for debugging purpose only
        min_x, max_x, min_y, max_y = self.shape()
        grid = self.grid[min_x:max_x + 1, min_y:max_y + 1]
        for y in range(grid.shape[1]):
            print(''.join([self.TILES[grid[x, y]] for x in range(grid.shape[0])]))


class Position(np.ndarray):
    """
    Position represent a coordinate on the grid
    """
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, (2,), dtype=int)

    def __init__(self, x=0, y=0):
        self[:] = [x, y]

    def set(self, x=0, y=0):
        self[:] = [x, y]

    def move(self, dx=0, dy=0):
        self[:] += [dx, dy]

    def __getattr__(self, item):
        # For convenience, we can access the 3 values by they name (.x, .y) to avoid to use of unclear indexes
        # like [0] or [1]
        try:
            if item in ['x', 'y']:
                return self[['x', 'y'].index(item)]
        except ValueError:
            raise AttributeError(f"No such attribute: {item}") from None


class Elf:
    """
    Elf represent an elf :
      - its current coordinate on the grid
      - its proposed coordinate on the grid, if the elf cannot move, its proposed coordinate will be same as its
        current coordinate
      - a direction index indicating in which indicating which direction to look first. An index of 0 will look in
        the following order: north, then south, then west and then east. An index of 1, will start by looking at
        south, and so on and so forth, until looping to north
    """
    DIRECTION_NORTH = 0
    DIRECTION_SOUTH = 1
    DIRECTION_WEST = 2
    DIRECTION_EAST = 3

    def __init__(self, grove, coord):
        self.grove = grove
        self.coord = coord
        self.proposed_coord = coord.copy()
        self.direction_index = -1

    def __repr__(self):
        return f"Elf({self.coord}#{self.proposed_coord}/{self.direction_index})"

    def move(self):
        self.coord[:] = self.proposed_coord

    def get_neighour(self, x, y):
        # Get a neighour cell on the grid according the x and y coordinate delta and returns its value
        # For instance get_neighour(0, -1) will look the cell at top of the grid just above (in other words,
        # look to the North)
        return self.grove.grid[self.coord.x + x, self.coord.y + y]

    def can_move(self):
        # Lookup the neighbourhood in all direction (N, S, E, W, SE, SW, NE and NW)
        # We put the value in a list,
        neighours = [
            self.get_neighour(0, -1), self.get_neighour(0, 1), self.get_neighour(-1, 0), self.get_neighour(1, 0),
            self.get_neighour(1, 1), self.get_neighour(-1, 1), self.get_neighour(1, -1), self.get_neighour(-1, -1)
        ]

        # The list has 8 values, if we don't have any elves in neighbourhood, all value must be equal to TILE_GROUND
        # So the sum of these values must be equal to TILE_GROUND * 8
        return sum(neighours) != 8 * Grove.TILE_GROUND

    def propose_move(self):
        self.direction_index += 1
        self.proposed_coord[:] = self.coord

        if not self.can_move():
            return

        for direction in range(self.direction_index, self.direction_index + 4):
            # Look in all 4 direction in that specific order: N, S, W and E
            # We start at direction index as described above and possibly
            # If no elf are in the concerned area for the direction, then we propose to move to that direction
            if direction % 4 == self.DIRECTION_NORTH:
                if self.get_neighour(-1, -1) == Grove.TILE_GROUND \
                        and self.get_neighour(0, -1) == Grove.TILE_GROUND \
                        and self.get_neighour(1, -1) == Grove.TILE_GROUND:
                    self.proposed_coord.move(0, -1)
                    break

            if direction % 4 == self.DIRECTION_SOUTH:
                if self.get_neighour(-1, 1) == Grove.TILE_GROUND \
                        and self.get_neighour(0, 1) == Grove.TILE_GROUND \
                        and self.get_neighour(1, 1) == Grove.TILE_GROUND:
                    self.proposed_coord.move(0, 1)
                    break

            if direction % 4 == self.DIRECTION_WEST:
                if self.get_neighour(-1, -1) == Grove.TILE_GROUND \
                        and self.get_neighour(-1, 0) == Grove.TILE_GROUND \
                        and self.get_neighour(-1, 1) == Grove.TILE_GROUND:
                    self.proposed_coord.move(-1, 0)
                    break

            if direction % 4 == self.DIRECTION_EAST:
                if self.get_neighour(1, -1) == Grove.TILE_GROUND \
                        and self.get_neighour(1, 0) == Grove.TILE_GROUND \
                        and self.get_neighour(1, 1) == Grove.TILE_GROUND:
                    self.proposed_coord.move(1, 0)
                    break


def day23_1(file):
    grove = Grove(file)
    grove.parse_grove()
    grove.run(max_round=10)
    print(grove.get_empty_ground_tiles())


def day23_2(file):
    grove = Grove(file)
    grove.parse_grove()
    print(grove.run())


if __name__ == '__main__':
    day23_1(sys.argv[1])
    day23_2(sys.argv[1])
