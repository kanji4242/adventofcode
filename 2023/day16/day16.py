#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/16
#

import sys
import numpy as np
from copy import copy


class Vector(tuple):
    """
    Vector subclass tuple with 2 values x and y
    It adds .x and .y properties for more code clarity
    """

    def __new__(cls, x=0, y=0):
        return super(Vector, cls).__new__(cls, tuple((x, y)))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]


class Coordinate:
    _move_vectors = [Vector(0, -1), Vector(1, 0), Vector(0, 1), Vector(-1, 0)]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coordinate({self.x}, {self.y})"

    def __copy__(self):
        return type(self)(self.x, self.y)

    def move(self, direction):
        self.x += self._move_vectors[direction].x
        self.y += self._move_vectors[direction].y


class Beam:
    DIRECTION_NORTH = 0
    DIRECTION_EAST = 1
    DIRECTION_SOUTH = 2
    DIRECTION_WEST = 3

    def __init__(self, coord, boundaries, direction):
        self.coord = coord
        self.boundaries = boundaries
        self.direction = direction

    def __repr__(self):
        return f"Beam(coord={self.coord}, direction={self.direction})"

    def move(self):
        turn_back = False

        if self.direction == self.DIRECTION_NORTH and self.coord.y == 0:
            turn_back = True
        elif self.direction == self.DIRECTION_EAST and self.coord.x == self.boundaries.x - 1:
            turn_back = True
        elif self.direction == self.DIRECTION_SOUTH and self.coord.y == self.boundaries.y - 1:
            turn_back = True
        elif self.direction == self.DIRECTION_WEST and self.coord.x == 0:
            turn_back = True

        if turn_back:
            self.direction = (self.direction + 2) % 4
        else:
            self.coord.move(self.direction)


class Layout:
    GRID_EMPTY = "."
    GRID_MIRROR_SLASH = "/"
    GRID_MIRROR_ANTI_SLASH = "\\"
    GRID_SPLITTER_VERT = "|"
    GRID_SPLITTER_HORZ = "-"

    def __init__(self):
        self.grid = None
        self.energized_grid = None
        self.beams = []
        self.boundaries = None
        self.mirror_history = []

    def _init_layout(self):
        self.energized_grid.fill(False)
        self.beams.clear()
        self.mirror_history.clear()

    def _nb_energized(self):
        return np.count_nonzero(self.energized_grid == True)

    def _has_beam_been_seen_in_mirror(self, beam):
        # This method is used to check whether a beam has previously passed through a specific mirror position
        # with a specific direction.

        # Iterate over each item in the mirror history
        for item in self.mirror_history:
            # Check if the current beam's position and direction match any item in the mirror history
            if beam.coord.x == item[0] and beam.coord.y == item[1] and beam.direction == item[2]:
                # If there's a match, return True indicating the beam has been seen in a mirror before
                return True
        # If no match is found, return False indicating the beam has not been seen in a mirror before
        return False

    def parse(self, file):
        with open(file) as f:
            size_x, size_y = 0, 0

            for line in f:
                size_x = max(size_x, len(line.rstrip()))
                size_y += 1

            # Initialize the array
            self.grid = np.ndarray((size_x, size_y), dtype=object)
            self.energized_grid = np.full((size_x, size_y), False, dtype=bool)

        # Second parse to fill the array
        with open(file) as f:
            y = 0
            for line in f:
                self.grid[:, y] = [ch for ch in line.rstrip()]
                y += 1

        self.boundaries = Coordinate(size_x, size_y)

    def move_beams(self):
        # Iterate over each beam in the list of beams
        for n in range(len(self.beams)):
            # Retrieve the current beam object
            beam = self.beams[n]

            # Mark the current position of the beam as energized on the energized grid
            self.energized_grid[beam.coord.x, beam.coord.y] = True

            # Check the type of obstacle the beam encounters and adjust its behavior accordingly
            if self.grid[beam.coord.x, beam.coord.y] == self.GRID_EMPTY:
                # If the cell is empty, move the beam forward
                beam.move()

            elif self.grid[beam.coord.x, beam.coord.y] == self.GRID_MIRROR_SLASH:
                # If the cell contains a mirror ('/'), change the beam direction accordingly and move forward
                # Direction changes are the following: 0 => 1, 1 => 0, 2 => 3, 3 => 2
                if (beam.direction % 2) == 0:
                    beam.direction = (beam.direction + 1) % 4
                else:
                    beam.direction = (beam.direction - 1) % 4
                beam.move()

            elif self.grid[beam.coord.x, beam.coord.y] == self.GRID_MIRROR_ANTI_SLASH:
                # If the cell contains a mirror ('\'), change the beam direction accordingly and move forward
                # Direction changes are the following: 0 => 3, 1 => 2, 2 => 1, 3 => 0
                if (beam.direction % 2) == 0:
                    beam.direction = (beam.direction - 1) % 4
                else:
                    beam.direction = (beam.direction + 1) % 4
                beam.move()

            elif self.grid[beam.coord.x, beam.coord.y] == self.GRID_SPLITTER_VERT:
                # If the cell contains a vertical splitter, split the beam vertically if it hasn't encountered
                # this splitter before
                if not self._has_beam_been_seen_in_mirror(beam):
                    if beam.direction == Beam.DIRECTION_EAST or beam.direction == Beam.DIRECTION_WEST:
                        # Record the current position and direction of the beam for future reference
                        self.mirror_history.append((beam.coord.x, beam.coord.y, beam.direction))
                        # Remove the current beam from the list
                        self.beams.pop(n)

                        # Create new beams moving respectively at north and south from the current position
                        # and move them
                        beam_north = Beam(copy(beam.coord), self.boundaries, Beam.DIRECTION_NORTH)
                        beam_north.move()
                        self.beams.append(beam_north)
                        beam_south = Beam(copy(beam.coord), self.boundaries, Beam.DIRECTION_SOUTH)
                        beam_south.move()
                        self.beams.append(beam_south)
                    else:
                        # If the beam is not moving along the splitter's axis, move it forward
                        beam.move()

            elif self.grid[beam.coord.x, beam.coord.y] == self.GRID_SPLITTER_HORZ:
                # If the cell contains a horizontal splitter, split the beam horizontally if it hasn't encountered
                # this splitter before
                if not self._has_beam_been_seen_in_mirror(beam):
                    if beam.direction == Beam.DIRECTION_SOUTH or beam.direction == Beam.DIRECTION_NORTH:
                        # Record the current position and direction of the beam for future reference
                        self.mirror_history.append((beam.coord.x, beam.coord.y, beam.direction))
                        # Remove the current beam from the list
                        self.beams.pop(n)

                        # Create new beams moving respectively at east and west from the current position
                        # and move them
                        beam_east = Beam(copy(beam.coord), self.boundaries, Beam.DIRECTION_EAST)
                        beam_east.move()
                        self.beams.append(beam_east)
                        beam_west = Beam(copy(beam.coord), self.boundaries, Beam.DIRECTION_WEST)
                        beam_west.move()
                        self.beams.append(beam_west)
                    else:
                        # If the beam is not moving along the splitter's axis, move it forward
                        beam.move()

    def activate_contraption(self, start_coord, direction):
        # This method activate the contraption, starting from a single beam at a specified coordinate and direction.
        # It iterates through a loop, moving beams according to certain rules until a termination condition is met.
        # The termination conditions include a maximum number of fixed energized cells or a maximum number of beams.

        # Initialize the layout, clearing any previous state
        self._init_layout()

        # Create a new beam starting at the specified coordinates and moving in the given direction
        self.beams = [Beam(copy(start_coord), self.boundaries, direction)]

        # Set the maximum number of times the number of energized cells is allowed to remain fixed
        nb_energized_p = None
        nb_energized_max_fixed = self.boundaries.x + self.boundaries.y

        # Main loop to propagate and handle the beams
        while True:
            # Count the number of energized cells in the grid
            nb_energized = self._nb_energized()

            # If the number of energized cells hasn't changed since the last iteration, decrease the
            # maximum fixed count
            if nb_energized_p and nb_energized == nb_energized_p:
                nb_energized_max_fixed -= 1

            # Move all beams according to the rules of the contraption
            self.move_beams()

            # If the maximum fixed count reaches zero, break out of the loop
            if nb_energized_max_fixed == 0:
                break

            # If the number of beams exceeds a certain threshold, break out of the loop to prevent infinite execution
            if len(self.beams) > 10_000:
                break

            # Update the previous number of energized cells
            nb_energized_p = nb_energized

        # Return the total count of energized cells in the grid
        return np.count_nonzero(self.energized_grid == True)

    def find_best_energized_configuration(self):
        # List to store the number of energized tiles for each configuration
        tiles_energized = []

        # Iterate over each tile in the top row and bottom row
        for start_coord_x in range(self.grid.shape[0]):
            # Activate the contraption starting by a beam located at a tile in the top row and heading downward
            tiles_energized.append(
                self.activate_contraption(Coordinate(start_coord_x, 0), Beam.DIRECTION_SOUTH))
            # Activate the contraption starting by a beam located at a tile in the top row and heading upward
            tiles_energized.append(
                self.activate_contraption(Coordinate(start_coord_x, self.grid.shape[1] - 1), Beam.DIRECTION_NORTH))

        # Iterate over each tile in the leftmost column and rightmost column
        for start_coord_y in range(self.grid.shape[1]):
            # Activate the contraption starting by a beam located at a tile in the leftmost column and heading right
            tiles_energized.append(
                self.activate_contraption(Coordinate(0, start_coord_y), Beam.DIRECTION_EAST))
            # Activate the contraption starting by a beam located at a tile in the rightmost column and heading left
            tiles_energized.append(
                self.activate_contraption(Coordinate(self.grid.shape[0] - 1, start_coord_y), Beam.DIRECTION_WEST))

        # Return the maximum number of energized tiles among all configurations
        return max(tiles_energized)

    def display_beams(self):
        direction_symbols = ['^', '>', 'v', '<']

        print(f"Layout {self.boundaries}")
        for y in range(self.grid.shape[1]):
            print(''.join([self.grid[x, y] for x in range(self.grid.shape[0])]))
        print("")

        for n in range(len(self.beams)):
            beam = self.beams[n]
            print(f"Beam {n} - {beam.coord}/{beam.direction}")
            line = ""
            for y in range(self.grid.shape[1]):
                for x in range(self.grid.shape[0]):
                    if beam.coord.x == x and beam.coord.y == y:
                        line += direction_symbols[beam.direction]
                    else:
                        line += "."

                line += "\n"

            print(line)
            print("")

    def display_energized(self):
        for y in range(self.energized_grid.shape[1]):
            print(''.join(["#" if self.energized_grid[x, y] else "." for x in range(self.energized_grid.shape[0])]))


def day16_1(file):
    layout = Layout()
    layout.parse(file)
    print(layout.activate_contraption(Coordinate(0, 0), Beam.DIRECTION_EAST))
    #layout.display_energized()


def day16_2(file):
    layout = Layout()
    layout.parse(file)
    print(layout.find_best_energized_configuration())

if __name__ == '__main__':
    day16_1(sys.argv[1])
    day16_2(sys.argv[1])

