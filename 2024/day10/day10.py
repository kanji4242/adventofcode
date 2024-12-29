#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2024/day/10
#

import sys
import numpy as np


class Coord:
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def __repr__(self):
        return f"Coord({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_upward(self):
        self.y -= 1

    def move_downward(self):
        self.y += 1


class HikingTrail:
    def __init__(self, grid, starting_coord):
        self.grid = grid
        self.coords = [starting_coord]

    def __repr__(self):
        return f"HikingTrail[{' '.join([repr(x) for x in self.coords])}]"

    def display_on_grid(self):
        # For debugging purpose, display the grid array
        for y in range(self.grid.shape[1]):
            line = ""
            for x in range(self.grid.shape[0]):
                line += f"[{self.grid[x, y]}] "
                ids = ''.join([str(id(coord))[-3:] + " " for coord in self.coords if coord.x == x and coord.y == y])
                line += ids
                line += " "*(16 - len(ids))

            print(line)
            print("")

    def add_coords(self, coord, avoid_duplicates=True):
        if avoid_duplicates:
            already_exists = False
            for c in self.coords:
                if coord.x == c.x and coord.y == c.y:
                    already_exists = True

            if not already_exists:
                self.coords.append(coord)
        else:
            self.coords.append(coord)

    def move_forward(self, part2=False):
        # Initialize a counter for the number of moves made.
        # This counter will determine if we were to move forward, meaning that we can continue.
        nb_moves = 0

        # Determine whether to avoid adding duplicate coordinates when adding new coordinates.
        # This is disabled for part 2
        avoid_duplicates = not part2

        # Iterate over the list of coordinates to move each one step forward.
        for i in range(len(self.coords)):
            # Get the current coordinate and create a copy for reference.
            current_coord = Coord((self.coords[i].x, self.coords[i].y))

            # Determine the next number to move towards based on the current coordinate.
            next_number = self.grid[current_coord.x, current_coord.y] + 1

            # Track whether a move has been made or whether new coordinates have been added.
            has_moved = False
            has_new_heads = False

            # Check if the next number exists to the left of the current coordinate.
            if current_coord.x > 0 and self.grid[current_coord.x - 1, current_coord.y] == next_number:
                # Move left if valid and set that we have moved.
                self.coords[i].move_left()
                has_moved = True

            # Check if the next number exists to the right of the current coordinate.
            if current_coord.x < self.grid.shape[0] - 1 and self.grid[
                current_coord.x + 1, current_coord.y] == next_number:
                if not has_moved:
                    # Move right if no other move has been made and set that we have moved.
                    self.coords[i].move_right()
                    has_moved = True
                else:
                    # Add a new coordinate for this path.
                    self.add_coords(Coord((current_coord.x + 1, current_coord.y)), avoid_duplicates=avoid_duplicates)
                    has_new_heads = True

            # Check if the next number exists above the current coordinate.
            if current_coord.y > 0 and self.grid[current_coord.x, current_coord.y - 1] == next_number:
                if not has_moved:
                    # Move upward if no other move has been made and set that we have moved.
                    self.coords[i].move_upward()
                    has_moved = True
                else:
                    # Add a new coordinate for this path.
                    self.add_coords(Coord((current_coord.x, current_coord.y - 1)), avoid_duplicates=avoid_duplicates)
                    has_new_heads = True

            # Check if the next number exists below the current coordinate.
            if current_coord.y < self.grid.shape[1] - 1 and self.grid[
                current_coord.x, current_coord.y + 1] == next_number:
                if not has_moved:
                    # Move downward if no other move has been made and set that we have moved.
                    self.coords[i].move_downward()
                    has_moved = True
                else:
                    # Add a new coordinate for this path.
                    self.add_coords(Coord((current_coord.x, current_coord.y + 1)), avoid_duplicates=avoid_duplicates)
                    has_new_heads = True

            # Increment the move counter if a move or a new path was created.
            if has_moved or has_new_heads:
                nb_moves += 1

        # If moves were made and duplicates should be avoided, deduplicate the coordinates (part 1 only).
        if nb_moves and not part2:
            self.coords = list(set(self.coords))

        # Return True if any moves were made, otherwise False.
        return True if nb_moves > 0 else False

    def score(self):
        # Extract the grid values at the coordinates in the trail.
        values = [self.grid[coord.x, coord.y] for coord in self.coords]

        # Return how many of these values are equal to 9.
        return values.count(9)


class HikingTrailGrid:
    def __init__(self):
        self.grid = None

    def parse_grid(self, file):
        with open(file) as f:
            size_x, size_y = 0, 0

            for line in f:
                size_x = max(size_x, len(line.rstrip()))
                size_y += 1

            # Initialize the array
            self.grid = np.ndarray((size_x, size_y), dtype=int)

        # Second parse to fill the array
        with open(file) as f:
            y = 0
            for line in f:
                self.grid[:, y] = [ch if ch != '.' else -1 for ch in line.rstrip()]
                y += 1

        return self.grid

    def find_hiking_trails(self, part2=False):
        hiking_trails = []

        # Find all starting coordinates where the grid value is 0.
        starting_coords = np.where(self.grid == 0)

        # Create a HikingTrail object for each starting coordinate.
        for starting_coord in list(zip(starting_coords[0], starting_coords[1])):
            hiking_trails.append(HikingTrail(self.grid, Coord(starting_coord)))

        # For each hiking trail, continue moving forward until no more moves are possible.
        for hiking_trail in hiking_trails:
            while hiking_trail.move_forward(part2=part2):
                pass

        # Calculate and print the total score for all hiking trails.
        print(sum([hiking_trail.score() for hiking_trail in hiking_trails]))


def day10_1(file):
    hiking_trail_grid = HikingTrailGrid()
    hiking_trail_grid.parse_grid(file)
    hiking_trail_grid.find_hiking_trails()


def day10_2(file):
    hiking_trail_grid = HikingTrailGrid()
    hiking_trail_grid.parse_grid(file)
    hiking_trail_grid.find_hiking_trails(part2=True)


if __name__ == '__main__':
    day10_1(sys.argv[1])
    day10_2(sys.argv[1])
