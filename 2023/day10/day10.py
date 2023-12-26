#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/10
#

import sys
import numpy as np

# Pipes constants
PIPE_V = 10
PIPE_H = 11
PIPE_B_NE = 12
PIPE_B_NW = 13
PIPE_B_SW = 14
PIPE_B_SE = 15
NO_PIPE = 0
STARTING_POINT = 1

PIPES = {
    "|": PIPE_V,
    "-": PIPE_H,
    "L": PIPE_B_NE,
    "J": PIPE_B_NW,
    "7": PIPE_B_SW,
    "F": PIPE_B_SE,
    ".": NO_PIPE,
    "S": STARTING_POINT
}

# Defines the connections of each pipe in the 4 directions of the Von Neumann neighborhood in the following order:
# [ north, east, south, west ]
PIPES_CONNECTIONS = {
    PIPE_V: (True, False, True, False),
    PIPE_H: (False, True, False, True),
    PIPE_B_NE: (True, True, False, False),
    PIPE_B_NW: (True, False, False, True),
    PIPE_B_SW: (False, False, True, True),
    PIPE_B_SE: (False, True, True, False),
    NO_PIPE: (False, False, False, False),
    STARTING_POINT: (True, True, True, True)
}


def convert_to_pipe(ch):
    if ch in PIPES:
        return PIPES[ch]


def is_straight_pipe(value):
    # Return True if a value is straight pipe (vertical or horizontal)
    return value in [PIPE_V, PIPE_H]


def is_corner_pipe(value):
    # Return True if a value is corner pipe (any of the 4 corner pipes)
    return value in [PIPE_B_NE, PIPE_B_NW, PIPE_B_SW, PIPE_B_SE]


def neighbourhood(area, coord):
    # Get the Von Neumann neighborhood coordinates of an array cell as a list in the following order:
    # [ north, east, south, west ]
    # Return None for coordinates that are out of bound
    x, y = coord
    size_x, size_y = area.shape

    return [
        (x, y - 1) if y > 0 else None,  # north
        (x + 1, y) if x < size_x - 1 else None,  # east
        (x, y + 1) if y < size_y - 1 else None,  # south
        (x - 1, y) if x > 0 else None  # west
    ]


def shoelace(coords):
    # Compute the area of a polygon using the shoelace formula (for part 2)
    nb_coords = len(coords)
    area = 0
    for i in range(nb_coords):
        j = (i + 1) % nb_coords
        area += coords[i][0] * coords[j][1]
        area -= coords[j][0] * coords[i][1]
    return abs(area) // 2


def display_area(area, current_coord, visited_coords=None):
    inverted_pipes = {v: k for k, v in PIPES.items()}

    for y in range(area.shape[1]):
        line = ""
        for x in range(area.shape[0]):
            if x == current_coord[0] and y == current_coord[1]:
                line += "\033[91m@\033[0m"
            if visited_coords and (x, y) in visited_coords:
                line += "\033[94m" + inverted_pipes[area[x][y]] + "\033[0m"
            else:
                line += inverted_pipes[area[x][y]]
        print(line)


def parse_file(file):
    with open(file) as f:
        size_x, size_y = 0, 0

        for line in f:
            size_x = max(size_x, len(line.rstrip()))
            size_y += 1

        # Initialize the array
        area = np.ndarray((size_x, size_y), dtype=int)

    # Second parse to fill the array
    with open(file) as f:
        y = 0
        for line in f:
            area[:, y] = [convert_to_pipe(ch) for ch in line.rstrip()]
            y += 1

    return area


def find_loop(area):
    # We start at the starting point ('S' character)
    starting_coord = tuple([x[0] for x in np.where(area == STARTING_POINT)])
    current_coord = starting_coord
    visited_coords = [current_coord]
    steps = 0
    nb_straight_pipes = 0
    nb_corner_pipes = 0

    while True:
        # We inspect the 4 neighbourhood cells and see if can connect a pipe
        # We already know that we have a single loop (no junction), Therefore if e find a connection, we can move on
        # to the next iteration and repeat the process until we go back the starting point
        nh_coords = neighbourhood(area, current_coord)
        connected = False

        # Connection north <-> south
        if nh_coords[0] and nh_coords[0] not in visited_coords \
                and PIPES_CONNECTIONS[area[current_coord]][0] is True \
                and PIPES_CONNECTIONS[area[nh_coords[0]]][2] is True:
            connected = True
            current_coord = nh_coords[0]

        # Connection east <-> west
        elif nh_coords[1] and nh_coords[1] not in visited_coords \
                and PIPES_CONNECTIONS[area[current_coord]][1] is True \
                and PIPES_CONNECTIONS[area[nh_coords[1]]][3] is True:
            connected = True
            current_coord = nh_coords[1]

        # Connection: south <-> north
        elif nh_coords[2] and nh_coords[2] not in visited_coords \
                and PIPES_CONNECTIONS[area[current_coord]][2] is True \
                and PIPES_CONNECTIONS[area[nh_coords[2]]][0] is True:
            connected = True
            current_coord = nh_coords[2]

        # Connection: west <-> east
        elif nh_coords[3] and nh_coords[3] not in visited_coords \
                and PIPES_CONNECTIONS[area[current_coord]][3] is True \
                and PIPES_CONNECTIONS[area[nh_coords[3]]][1] is True:
            connected = True
            current_coord = nh_coords[3]

        if connected:
            # If we have found a connection, we update the current position and loopback
            visited_coords.append(current_coord)
            steps += 1

            # This is for the part 2, we need to keep track of the number of straight pipes and corner pipes
            # So we update the counters here
            if is_straight_pipe(area[current_coord]):
                nb_straight_pipes += 1
            elif is_corner_pipe(area[current_coord]):
                nb_corner_pipes += 1

        else:
            # Otherwise, we consider that we have completed the loop and stop here
            break

    # We have deliberately not counted the pipe from the starting point because we don't know its type at
    # the beginning of the process. Since we now have the coordinates of the complete loop, we can do so here
    if current_coord[0] == visited_coords[1][0] or current_coord[1] == visited_coords[1][1]:
        nb_straight_pipes += 1
    else:
        nb_corner_pipes += 1

    return visited_coords, nb_straight_pipes, nb_corner_pipes


def find_farthest_point(visited_coords):
    # The farthest point is easy to compute, we just have to count the number of visited coordinates and divide it by 2
    return len(visited_coords) // 2


def find_enclosed_area(visited_coords, nb_straight_pipes, nb_corner_pipes):
    # For the part 2, my method rely on the shoelace formula and the formula for the sum of the angles of a polygon
    # The idea is to consider the area as 2D place and consider the loop coordinates as vertex and sides of a
    # polygon. This will help us because we can compute its area with the
    # shoelace formula. But there is a problem, the computed area will be too big, because the vertex and the sides
    # we imagine are located "in the middle" of the cell boundaries, so we have extra area. We need to subtract this
    # extra area. I found a trick to have a simple formula. It is based on the fact that the sum of the angles of a
    # n-gon polygon is always the same. We just have to count the number of vertex which correspond to corner pipes
    # and consider the following every 90° angles have an area of 1/4, and every straight pipes are assumed to be
    # part of the side of the polygon and have area of 1/2.
    # The formula for the sum of the angles of a polygon is : 180° + (nb_of_vertex - 3) * 180°
    area = shoelace(visited_coords) - (nb_straight_pipes + (1 + (nb_corner_pipes - 3))) // 2
    return area


def day10_1(file):
    visited_coords, nb_straight_pipes, nb_corner_pipes = find_loop(parse_file(file))
    print(find_farthest_point(visited_coords))


def day10_2(file):
    visited_coords, nb_straight_pipes, nb_corner_pipes = find_loop(parse_file(file))
    print(find_enclosed_area(visited_coords, nb_straight_pipes, nb_corner_pipes))


if __name__ == '__main__':
    day10_1(sys.argv[1])
    day10_2(sys.argv[1])
