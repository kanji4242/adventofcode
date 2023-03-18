#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/23
#

import sys
import numpy as np
from pprint import pprint


class Grove:
    TILE_GROUND = 0
    TILE_ELF = 1

    TILES = {
        TILE_GROUND: '.',
        TILE_ELF: '#',
    }

    def __init__(self, file):
        self.file = file
        self.grid = None
        self.new_grid = None
        self.elves = []

    def parse_grove(self):
        extra_shape = 10
        with open(self.file) as f:
            size_x, size_y = 0, 0

            for line in f:
                size_x = max(size_x, len(line.rstrip()))
                size_y += 1

        self.grid = np.ndarray((size_x * (2 * extra_shape + 1), size_y * (2 * extra_shape + 1)), dtype=int)
        self.new_grid = self.grid.copy()
        tiles_reverse = {v: k for k, v in self.TILES.items()}

        with open(self.file) as f:
            y = 2 * extra_shape
            for line in f:
                line = line.rstrip()
                self.grid[:, y] = [self.TILE_GROUND] * (size_x * extra_shape) + [tiles_reverse[x] for x in line] +\
                                  [self.TILE_GROUND] * (size_x * extra_shape)
                y += 1

        for y in range(self.grid.shape[1]):
            for x in range(self.grid.shape[0]):
                if self.grid[x, y] == self.TILE_ELF:
                    self.elves.append(Elf(self, Position(x, y)))

    def run(self, max_round=None):
        nb_round = 0
        while True:
            nb_round += 1
            nb_moves = self.do_turn()
            if nb_moves == 0 or (max_round is not None and nb_round >= max_round):
                break
            print(nb_round, nb_moves)

        return nb_round

    def do_turn(self):
        proposed_moves = {}
        nb_moves = 0

        for elf in self.elves:
            elf.propose_move()

        for elf in self.elves:
            proposed_move = tuple(elf.proposed_coord)
            if proposed_move not in proposed_moves:
                proposed_moves[proposed_move] = [elf]
            else:
                proposed_moves[proposed_move].append(elf)

        #pprint(self.elves)
        #pprint(proposed_moves)

        self.new_grid.fill(self.TILE_GROUND)

        for coord, elves in proposed_moves.items():
            if len(elves) > 1:
                for elf in elves:
                    self.new_grid[tuple(elf.coord)] = self.TILE_ELF
            else:
                self.new_grid[tuple(elves[0].proposed_coord)] = self.TILE_ELF
                if elves[0].coord.x != elves[0].proposed_coord.x or elves[0].coord.y != elves[0].proposed_coord.y:
                    nb_moves += 1

                elves[0].move()

        self.grid, self.new_grid = self.new_grid, self.grid

        #print("moves:", nb_moves)
        return nb_moves

    def shape(self):
        min_x, max_x = self.elves[0].coord.x, self.elves[0].coord.x
        min_y, max_y = self.elves[0].coord.y, self.elves[0].coord.y

        for y in range(self.grid.shape[1]):
            for x in range(self.grid.shape[0]):
                if self.grid[x, y] == self.TILE_ELF:
                    min_x, max_x = min(x, min_x), max(x, max_x)
                    min_y, max_y = min(y, min_y), max(y, max_y)

        print(min_x, max_x, min_y, max_y)
        return min_x, max_x, min_y, max_y

    def get_empty_ground_tiles(self):
        min_x, max_x, min_y, max_y = self.shape()

        return np.count_nonzero(self.grid[min_x:max_x + 1, min_y:max_y + 1] == self.TILE_GROUND)

    def display_grove(self):
        min_x, max_x, min_y, max_y = self.shape()
        grid = self.grid[min_x:max_x + 1, min_y:max_y + 1]
        for y in range(grid.shape[1]):
            print(''.join([self.TILES[grid[x, y]] for x in range(grid.shape[0])]))


class Position(np.ndarray):
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
        return self.grove.grid[self.coord.x + x, self.coord.y + y]

    def can_move(self):
        neighours = [
            self.get_neighour(0, -1), self.get_neighour(0, 1), self.get_neighour(-1, 0), self.get_neighour(1, 0),
            self.get_neighour(1, 1), self.get_neighour(-1, 1), self.get_neighour(1, -1), self.get_neighour(-1, -1)
        ]

        return sum(neighours) != 8 * Grove.TILE_GROUND

    def propose_move(self):
        #print(self.coord, "propose_move")
        self.direction_index += 1
        self.proposed_coord[:] = self.coord

        if not self.can_move():
            return

        for direction in range(self.direction_index, self.direction_index + 4):
            if direction % 4 == self.DIRECTION_NORTH and self.coord.y > 0:
                if self.get_neighour(-1, -1) == Grove.TILE_GROUND \
                        and self.get_neighour(0, -1) == Grove.TILE_GROUND \
                        and self.get_neighour(1, -1) == Grove.TILE_GROUND:
                    #print(self.coord, "propose north")
                    self.proposed_coord.move(0, -1)
                    break

            if direction % 4 == self.DIRECTION_SOUTH and self.coord.y < self.grove.grid.shape[1] - 1:
                if self.get_neighour(-1, 1) == Grove.TILE_GROUND \
                        and self.get_neighour(0, 1) == Grove.TILE_GROUND \
                        and self.get_neighour(1, 1) == Grove.TILE_GROUND:
                    #print(self.coord, "propose south")
                    self.proposed_coord.move(0, 1)
                    break

            if direction % 4 == self.DIRECTION_WEST and self.coord.x > 0:
                if self.get_neighour(-1, -1) == Grove.TILE_GROUND \
                        and self.get_neighour(-1, 0) == Grove.TILE_GROUND \
                        and self.get_neighour(-1, 1) == Grove.TILE_GROUND:
                    #print(self.coord, "propose west")
                    self.proposed_coord.move(-1, 0)
                    break

            if direction % 4 == self.DIRECTION_EAST and self.coord.x < self.grove.grid.shape[0] - 1:
                if self.get_neighour(1, -1) == Grove.TILE_GROUND \
                        and self.get_neighour(1, 0) == Grove.TILE_GROUND \
                        and self.get_neighour(1, 1) == Grove.TILE_GROUND:
                    #print(self.coord, "propose east")
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
    #grove.display_grove()
    print(grove.run())


if __name__ == '__main__':
    day23_1(sys.argv[1])
    day23_2(sys.argv[1])
