#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/24
#

import sys
import numpy as np


class Vector(tuple):
    """
    Vector subclass tuple with 2 values x and y
    It add .x and .y property for more code clarity
    """
    def __new__ (cls, x=0, y=0):
        return super(Vector, cls).__new__(cls, tuple((x, y)))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]


class Valley:
    """
    Grove represents a grove with:
      - the 2 grids (numpy array) where elves will be placed, the first one is active while the second one is inactive,
        as described above.
      - a list of elves
    """
    TILE_GROUND = 0
    TILE_BZ_UP = 1
    TILE_BZ_DOWN = 2
    TILE_BZ_LEFT = 4
    TILE_BZ_RIGHT = 8
    TILE_WALL = 64

    TILES = {
        TILE_GROUND: '.',
        TILE_BZ_UP: '^',
        TILE_BZ_DOWN: 'v',
        TILE_BZ_LEFT: '<',
        TILE_BZ_RIGHT: '>',
        TILE_WALL: '#',
    }

    BZ_TILE_EMPTY = 0
    BZ_TILE_WIND = 1

    BZ_TILES = {
        BZ_TILE_EMPTY: ".",
        BZ_TILE_WIND: "O",
    }
    BZ_GRID_TILES_ID = [1, 2, 4, 8]
    BZ_GRID_VECTORS = [
        Vector(0, -1),
        Vector(0, 1),
        Vector(-1, 0),
        Vector(1, 0),
    ]

    def __init__(self, file):
        self.file = file
        self.minute = 0

        # Grid of the valley
        self.grid = None
        # Previous grid of the valley, contain the valley configuration 1 minute before
        # Every a new minute is increment self.grid is copied to self.prev_grid
        self.prev_grid = None

        # Grids for breeze (will contain 4 grids for the 4 directions)
        self.bz_grid = []

        # Distances matrix to compute the optimum path
        self.distances = None
        # The new distances matrix that will set for the current minute
        self.new_distances = None

        # Start and end coordinate on the grid of the valley
        self.start_coord = None
        self.end_coord = None

    def parse_input(self):
        # First parse the input file to get the original size
        with open(self.file) as f:
            size_x, size_y = 0, 0

            for line in f:
                size_x = max(size_x, len(line.rstrip()))
                size_y += 1

        # Build the grid with extra room
        self.grid = np.ndarray((size_x, size_y), dtype=int)

        for i in range(4):
            bzgrid = np.ndarray((size_x - 2, size_y - 2), dtype=int)
            bzgrid.fill(self.BZ_TILE_EMPTY)
            self.bz_grid.append(bzgrid)

        tiles_reverse = {v: k for k, v in self.TILES.items()}

        # Parse the input file again and place the elves directly from the line read
        with open(self.file) as f:
            y = 0
            for line in f:
                for x in range(len(line.rstrip())):
                    self.grid[x, y] = tiles_reverse[line[x]]
                    if 0 < tiles_reverse[line[x]] < self.TILE_WALL:
                        index = self.BZ_GRID_TILES_ID.index(tiles_reverse[line[x]])
                        self.bz_grid[index][x - 1, y - 1] = self.BZ_TILE_WIND
                if y == 0:
                    # Find where we have a ground cell (TILE_GROUND) on the first line, this is where the start
                    # coordinate is
                    self.start_coord = (int(np.where(self.grid[:, 0] == self.TILE_GROUND)[0]), 0)
                y += 1

            # In the same way as start coordinate, find where we have a ground cell (TILE_GROUND) on the last
            # line, this is where the end coordinate is
            self.end_coord = (int(np.where(self.grid[:, y - 1] == self.TILE_GROUND)[0]), y - 1)

        # Build the distance and initialize it
        self.distances = np.ndarray((size_x, size_y), dtype=int)
        self.init_distances()

        self.build_valley()

    def build_valley(self):
        # Build the grid valley grid from the 4 breeze grids
        self.prev_grid = self.grid.copy()

        for y in range(self.grid.shape[1] - 2):
            for x in range(self.grid.shape[0] - 2):
                value = 0
                for i in range(len(self.BZ_GRID_TILES_ID)):
                    bz_grid_x = (x - self.BZ_GRID_VECTORS[i].x * self.minute) % (self.bz_grid[i].shape[0])
                    bz_grid_y = (y - self.BZ_GRID_VECTORS[i].y * self.minute) % (self.bz_grid[i].shape[1])
                    if self.bz_grid[i][bz_grid_x, bz_grid_y]:
                        # The value is a binary value, each bit represents a breeze direction and is set to 1
                        # if the breeze is present
                        value |= 1 << i
                self.grid[x + 1, y + 1] = value

    def update_distances(self):
        for y in range(self.grid.shape[1]):
            for x in range(self.grid.shape[0]):
                if self.grid[x, y] == self.TILE_GROUND:
                    for direction in [Vector(0, 0), Vector(1, 0), Vector(-1, 0), Vector(0, 1), Vector(0, -1)]:
                        if 0 <= x + direction.x < self.grid.shape[0] and 0 <= y + direction.y < self.grid.shape[1]:
                            if self.distances[x + direction.x, y + direction.y] == self.minute - 1:
                                self.new_distances[x, y] = self.minute
        self.distances = self.new_distances.copy()

    def tiles(self, value):
        if int(value) in self.TILES.keys():
            return self.TILES[value]
        else:
            return "2"

    def inverse_direction(self):
        self.start_coord, self.end_coord = self.end_coord, self.start_coord
        self.init_distances()

    def init_distances(self):
        # Initialize the distances by filling all value to -1
        self.distances.fill(-1)
        # The start coordinate with set to the current minute
        self.distances[self.start_coord] = self.minute
        self.new_distances = self.distances.copy()

    def do_round(self):
        while True:
            self.minute += 1
            #print("minute", self.minute)
            self.build_valley()
            self.update_distances()

            if self.distances[self.end_coord] != -1:
                break

    def display_valley(self, display_bz_graph=False):
        # Display the valley for debugging purpose only
        for y in range(self.grid.shape[1]):
            print(''.join([self.tiles(self.grid[x, y]) for x in range(self.grid.shape[0])]))

        print(" ")
        if display_bz_graph:
            for i in range(4):
                for y in range(self.bz_grid[i].shape[1]):
                    print(''.join([self.BZ_TILES[self.bz_grid[i][x, y]] for x in range(self.bz_grid[i].shape[0])]))
                print(" ")

    def display_distances(self):
        # Display the distance matrix for debugging purpose only
        for y in range(self.distances.shape[1]):
            print(''.join([f"{self.distances[x, y]:3}" for x in range(self.distances.shape[0])]))


def day24_1(file):
    v = Valley(file)
    v.parse_input()
    v.do_round()
    print(v.minute)


def day24_2(file):
    v = Valley(file)
    v.parse_input()
    v.do_round()
    v.inverse_direction()
    v.do_round()
    v.inverse_direction()
    v.do_round()
    print(v.minute)


if __name__ == '__main__':
    day24_1(sys.argv[1])
    day24_2(sys.argv[1])
