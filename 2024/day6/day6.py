#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2024/day/6
#

import sys
import numpy as np
import re


class LabGrid:
    GRID_EMPTY = 0
    GRID_OBSTRUCT = 1

    GRID = {
        '.': GRID_EMPTY,
        '#': GRID_OBSTRUCT
    }
    GUARD_DIRECTIONS = ['^', '>', 'v', '<']
    GUARD_VECTORS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __init__(self, file):
        self.file = file
        self.grid = None
        self.guard_direction = 0
        self.guard_position = [0, 0]
        self.guard_initial_position = 0
        self.guard_initial_direction = [0, 0]
        self.visited_position = []

    def display_grid(self):
        # For debugging purpose, display the grid array
        inverted_grid = {v: k for k, v in self.GRID.items()}

        for y in range(self.grid.shape[1]):
            cells = [inverted_grid[self.grid[x, y]] for x in range(self.grid.shape[0])]
            if self.guard_position[1] == y:
                cells[self.guard_position[0]] = self.GUARD_DIRECTIONS[self.guard_direction]
            print(''.join(cells))

        print(self.guard_position)

    def parse_grid(self):
        with open(self.file) as f:
            size_x, size_y = 0, 0

            for line in f:
                size_x = max(size_x, len(line.rstrip()))
                size_y += 1

            # Initialize the array
            self.grid = np.ndarray((size_x, size_y), dtype=int)

        # Second parse to fill the array
        with open(self.file) as f:
            y = 0
            for line in f:
                line = line.rstrip()
                for x in range(len(line)):
                    if line[x] in self.GUARD_DIRECTIONS:
                        self.guard_direction = self.GUARD_DIRECTIONS.index(line[x])
                        self.guard_position[0], self.guard_position[1] = x, y
                        self.grid[x, y] = self.GRID_EMPTY
                    else:
                        self.grid[x, y] = self.GRID[line[x]]
                y += 1

        self.guard_initial_position = self.guard_position[:]
        self.guard_initial_direction = self.guard_direction


    def move_guard(self):
        next_position = self.guard_position[:]  # Copy the current guard position
        nb_position = 1  # Counter for unique positions visited
        # Initialize the list of visited positions with the current guard position
        self.visited_position = [(self.guard_position[0], self.guard_position[1])]

        # Move the guard until his next position is outside the grid bounds
        while True:
            # Determine the movement vector based on the guard's current direction
            move_vector = self.GUARD_VECTORS[self.guard_direction]
            # Calculate the next position based on the movement vector
            next_position[0] = self.guard_position[0] + move_vector[0]
            next_position[1] = self.guard_position[1] + move_vector[1]

            # Check if the next position is within the grid bounds
            if not (0 <= next_position[0] < self.grid.shape[0] and 0 <= next_position[1] < self.grid.shape[1]):
                break  # Stop the movement

            # Check if the next position is obstructed
            if self.grid[next_position[0], next_position[1]] == self.GRID_OBSTRUCT:
                # Reset the next position to the current position
                next_position[0], next_position[1] = self.guard_position[0], self.guard_position[1]
                # Change the guard's direction (rotate 90° clockwise)
                self.guard_direction = (self.guard_direction + 1) % 4
            else:
                # Move the guard to the new position
                self.guard_position[0], self.guard_position[1] = next_position[0], next_position[1]
                # If the new position has not been visited yet
                if (next_position[0], next_position[1]) not in self.visited_position:
                    nb_position += 1  # Increment the count of unique positions visited
                    self.visited_position.append((next_position[0], next_position[1]))  # Mark it as visited

        return nb_position

    def reset_position(self):
        # Reset the position
        self.guard_position[0], self.guard_position[1] = self.guard_initial_position[0], self.guard_initial_position[1]
        self.guard_direction = self.guard_initial_direction

    def find_loops(self):
        nb_loops = 0

        self.move_guard()
        self.reset_position()

        for x, y in self.visited_position:
            self.grid[x, y] = self.GRID_OBSTRUCT
            if self.move_guard_with_direction():
                nb_loops += 1

            self.reset_position()
            self.grid[x, y] = self.GRID_EMPTY

        return nb_loops

    def move_guard_with_direction(self):
        # Same algorithm as move_guard() but with direction recorded to detect loops

        next_position = self.guard_position[:]  # Copy the current guard position
        is_loop = False

        # Initialize the list of visited positions with the current guard position
        visited_position_with_direction = [(self.guard_position[0], self.guard_position[1], self.guard_direction)]

        # Move the guard until his next position is outside the grid bounds
        while True:
            # Determine the movement vector based on the guard's current direction
            move_vector = self.GUARD_VECTORS[self.guard_direction]
            # Calculate the next position based on the movement vector
            next_position[0] = self.guard_position[0] + move_vector[0]
            next_position[1] = self.guard_position[1] + move_vector[1]

            # Check if the next position is within the grid bounds
            if not (0 <= next_position[0] < self.grid.shape[0] and 0 <= next_position[1] < self.grid.shape[1]):
                break  # Stop the movement

            # Check if the next position is obstructed
            if self.grid[next_position[0], next_position[1]] == self.GRID_OBSTRUCT:
                # Reset the next position to the current position
                next_position[0], next_position[1] = self.guard_position[0], self.guard_position[1]
                # Change the guard's direction (rotate 90° clockwise)
                self.guard_direction = (self.guard_direction + 1) % 4
            else:
                # Move the guard to the new position
                self.guard_position[0], self.guard_position[1] = next_position[0], next_position[1]
                # If the new position has not been visited yet and the direction is not the same
                if (next_position[0], next_position[1], self.guard_direction) not in visited_position_with_direction:
                    visited_position_with_direction.append((next_position[0], next_position[1], self.guard_direction))
                else:
                    # Otherwise it's a loop
                    is_loop = True
                    break

        return is_loop

def day6_1(file):
    labgrid = LabGrid(file)
    labgrid.parse_grid()
    print(labgrid.move_guard())


def day6_2(file):
    labgrid = LabGrid(file)
    labgrid.parse_grid()
    print(labgrid.find_loops())


if __name__ == '__main__':
    day6_1(sys.argv[1])
    day6_2(sys.argv[1])
