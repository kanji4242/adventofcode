#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/24
#

"""
The idea is to build several grids:
 - a valley grid, which contains all the data in the input file
 - 4 grids that contain the position of the blizzards in the 4 directions
 - a distance matrix of the same size as the valley grid and containing the distances that can be traveled as the
   minutes pass. Each value in the matrix contains the number of minutes required to reach a particular location.


The valley grid will include wall, and grounds and blizzards. Since they can be several blizzards at a given position,
we use a bit-wise value which allows the detection hwo many blizzards we have in that position. We use the following
values: 1 for up, 2 for down, 4 for left and 8 for right motions, 64 for walls, a clear ground will then have a value
of 0.

On the given exemple at its initial state will look like:

 64  0 64 64 64 64 64 64
 64  8  8  0  4  1  4 64
 64  0  4  0  0  4  4 64
 64  8  2  0  8  4  8 64
 64  4  1  2  1  1  8 64
 64 64 64 64 64 64  0 64

At this stage, we don't have any position with more than 1 blizzards (all value are a power of 2), but at minute 1,
we will:

 64  0 64 64 64 64 64 64
 64  0  8 14  0  4  0 64
 64  4  0  0  4  4  0 64
 64  8  9  0  5  9  0 64
 64  8  2  0  0  1  4 64
 64 64 64 64 64 64  0 64

The 4 blizzards grids will contain only the position of the blizzards. Since walls are surrounding the valley, their size
will be the same as the valley grid minus 2.

On the given example, the 4 grids will look like this:

 Up motion      Down motion   Left motion   Right motion

 ....^.         ......        ...<.<        >>....
 ......         ......        .<..<<        ......
 ......         .v....        ....<.        >..>.>
 .^.^^.         ..v...        <.....        .....>

The valley grid is built each minute from the 4 blizzard grids according to the blizzard progression.

To simulate the blizzard progression, it is not necessary to modify the grid. You just have to read each grid from an
index incremented every minute modulo the size of the grid.

The distance matrix is filled with -1, except for the starting point which is initially with the current minute (0 at
the beginning, but may different in part 2). The distance matrix is updated each minute.

On the given example, the distance matrix will look like this:

 -1  0 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1

Since we're starting at (1, 0), the value at this position is set to 0.

Each minute, we identify where we have clean ground on the valley grid. For each position found, we then look at the
distance at 5 positions: at the position found, at the position below, at the position above, at the position on the
left, and at the position on the right.

If we found a cell with contains the previous minute value (minute - 1), we then update that cell with the current
minute value. With this iterating process each minute, we have the minimum number of minutes required to reach a
particular position.

On the same example, at minute 1, we are able to go down, so we will have 2 ones:

 -1  1 -1 -1 -1 -1 -1 -1
 -1  1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1

On minute 2, we're also able to go down, so we will have 3 twos:

 -1  2 -1 -1 -1 -1 -1 -1
 -1  2 -1 -1 -1 -1 -1 -1
 -1  2 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1

We stop until we reach the ending position and have a minimum number of minutes for it.

Here is the final state (at minute 18):

 -1 18 -1 -1 -1 -1 -1 -1
 -1 16 17 18 17 18 15 -1
 -1 18 17 16 17 17 16 -1
 -1 17 18 13 14 15 16 -1
 -1 17 18 14 -1 18 17 -1
 -1 -1 -1 -1 -1 -1 18 -1

To go backward for part 2, this is very straightforward. We just need to invert the starting and end position and
reinitialize the matrix as described above. Since we're on the run, we will then have a value greater than 0 on the
starting point:

 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 -1 -1
 -1 -1 -1 -1 -1 -1 18 -1

And repeat the same iteration.


"""

import sys
import numpy as np


class Vector(tuple):
    """
    Vector subclass tuple with 2 values x and y
    It adds .x and .y property for more code clarity
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

        # Grids for blizzard (will contain 4 grids for the 4 directions)
        self.bz_grid = []

        # Distances matrix to compute the optimum path
        self.distances = None
        # The new distances matrix that will be built for the current minute
        # We do this because the detection algorithm will be affected while updating the matrix, so we need to
        # work on a new copy
        self.new_distances = None

        # Start and end position on the grid of the valley
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
            bz_grid = np.ndarray((size_x - 2, size_y - 2), dtype=int)
            bz_grid.fill(self.BZ_TILE_EMPTY)
            self.bz_grid.append(bz_grid)

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
                    # position is
                    self.start_coord = (int(np.where(self.grid[:, 0] == self.TILE_GROUND)[0]), 0)
                y += 1

            # In the same way as start position, find where we have a ground cell (TILE_GROUND) on the last
            # line, this is where the end position is
            self.end_coord = (int(np.where(self.grid[:, y - 1] == self.TILE_GROUND)[0]), y - 1)

        # Build the distance and initialize it
        self.distances = np.ndarray((size_x, size_y), dtype=int)
        self.init_distances()

        self.build_valley()

    def build_valley(self):
        # Build the grid valley grid from the 4 blizzard grids
        for y in range(self.grid.shape[1] - 2):
            for x in range(self.grid.shape[0] - 2):
                value = 0
                for i in range(len(self.BZ_GRID_TILES_ID)):
                    # We simulate the blizzard progression by reading the blizzard with incremented index
                    # Depending on blizzard motion, the index on x-axis will be incremented for left and right blizzard
                    # while the index on y-axis will be incremented for up and down
                    bz_grid_x = (x - self.BZ_GRID_VECTORS[i].x * self.minute) % (self.bz_grid[i].shape[0])
                    bz_grid_y = (y - self.BZ_GRID_VECTORS[i].y * self.minute) % (self.bz_grid[i].shape[1])
                    if self.bz_grid[i][bz_grid_x, bz_grid_y]:
                        # The value is a binary value, each bit represents a blizzard direction and is set to 1
                        # if the blizzard is present
                        value |= 1 << i
                self.grid[x + 1, y + 1] = value

    def update_distances(self):
        for y in range(self.grid.shape[1]):
            for x in range(self.grid.shape[0]):
                if self.grid[x, y] == self.TILE_GROUND:
                    # We found a clear ground with no blizzard
                    for direction in [Vector(0, 0), Vector(1, 0), Vector(-1, 0), Vector(0, 1), Vector(0, -1)]:
                        # We look at the position found, at the position below, at the position above,
                        # at the position on the and at the position on the right.
                        # We also check the boundary of the matrix
                        if 0 <= x + direction.x < self.grid.shape[0] and 0 <= y + direction.y < self.grid.shape[1]:
                            # If we found a cell with contains the previous minute value (minute - 1), we then
                            # update that cell with the current minute value.
                            if self.distances[x + direction.x, y + direction.y] == self.minute - 1:
                                self.new_distances[x, y] = self.minute

        self.distances = self.new_distances.copy()

    def inverse_direction(self):
        self.start_coord, self.end_coord = self.end_coord, self.start_coord
        self.init_distances()

    def init_distances(self):
        # Initialize the distances by filling all values to -1
        self.distances.fill(-1)
        # The start position with set to the current minute
        self.distances[self.start_coord] = self.minute
        self.new_distances = self.distances.copy()

    def travel(self):
        while True:
            self.minute += 1
            #print("minute", self.minute)
            self.build_valley()
            self.update_distances()

            if self.distances[self.end_coord] != -1:
                break

    def tiles(self, value):
        # Find which character to display for a ground cell (for debugging purpose only=)
        if int(value) in self.TILES.keys():
            return self.TILES[value]
        else:
            # If we have more than 1 blizzard on the cell we display "2" by default
            return "2"

    def display_valley(self, display_bz_graph=False):
        # Display the valley (for debugging purpose only=)
        for y in range(self.grid.shape[1]):
            print(''.join([self.tiles(self.grid[x, y]) for x in range(self.grid.shape[0])]))

        for y in range(self.grid.shape[1]):
            print(''.join([f"{self.grid[x, y]:3}" for x in range(self.grid.shape[0])]))

        print(" ")
        if display_bz_graph:
            for i in range(4):
                for y in range(self.bz_grid[i].shape[1]):
                    print(''.join([self.BZ_TILES[self.bz_grid[i][x, y]] for x in range(self.bz_grid[i].shape[0])]))
                print(" ")

    def display_distances(self):
        # Display the distance matrix (for debugging purpose only=)
        for y in range(self.distances.shape[1]):
            print(''.join([f"{self.distances[x, y]:3}" for x in range(self.distances.shape[0])]))
        print(" ")


def day24_1(file):
    v = Valley(file)
    v.parse_input()
    v.travel()
    print(v.minute)


def day24_2(file):
    v = Valley(file)
    v.parse_input()
    v.travel()
    v.inverse_direction()
    v.travel()
    v.inverse_direction()
    v.travel()
    print(v.minute)


if __name__ == '__main__':
    day24_1(sys.argv[1])
    day24_2(sys.argv[1])
