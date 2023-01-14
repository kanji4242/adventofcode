#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/14
#

import sys
import numpy as np

CELL_AIR = 0
CELL_WALL = 1
CELL_SAND = 2
CELL_POUR = 3
POUR_X = 500
POUR_Y = 0


def symbol(cell):
    cell_map = {CELL_AIR: '.', CELL_WALL: '#', CELL_SAND: 'o', CELL_POUR: '+'}
    return cell_map[cell]


def display_grid(grid, offsetx=0, offsety=0):
    for y in range(offsety, grid.shape[1]):
        print(''.join([symbol(grid[x][y]) for x in range(offsetx, grid.shape[0])]))


def xrange(start, end):
    if start == end:
        return range(start, end)
    elif start > end:
        return range(start, end - 1, -1)
    else:
        return range(start, end + 1)


def parse_paths(file, add_floor=False):
    with open(file) as f:
        line_paths = []
        for line in f:
            line_paths.append([tuple([int(y) for y in x.split(",")]) for x in line.strip().split(" -> ")])

    max_x = max([y[0] for x in line_paths for y in x])
    max_y = max([y[1] for x in line_paths for y in x])
    grid = np.zeros((max_x + max_y + 2, max_y + 3), dtype=int)

    for path in line_paths:
        for x in range(len(path) - 1):
            if path[x][0] == path[x + 1][0]:
                for i in xrange(path[x][1], path[x + 1][1]):
                    grid[path[x][0]][i] = CELL_WALL
            elif path[x][1] == path[x + 1][1]:
                for i in xrange(path[x][0], path[x + 1][0]):
                    grid[i][path[x][1]] = CELL_WALL

    grid[POUR_X][0] = CELL_POUR

    if add_floor:
        for x in range(grid.shape[0]):
            grid[x][max_y + 2] = CELL_WALL

    return grid


def pour_sand(grid, return_blocked=False):
    sand_offset_x, sand_offset_y = POUR_X, POUR_Y
    in_void = False
    blocked = False

    while True:
        if sand_offset_y >= (grid.shape[1] - 1):
            in_void = True
            break

        if grid[sand_offset_x][sand_offset_y + 1] == CELL_AIR:
            sand_offset_y += 1
        else:
            if grid[sand_offset_x - 1][sand_offset_y + 1] == CELL_AIR:
                sand_offset_x -= 1
                sand_offset_y += 1
            elif grid[sand_offset_x + 1][sand_offset_y + 1] == CELL_AIR:
                sand_offset_x += 1
                sand_offset_y += 1
            else:
                grid[sand_offset_x][sand_offset_y] = CELL_SAND
                if sand_offset_x == POUR_X and sand_offset_y == POUR_Y:
                    blocked = True
                break

    if return_blocked:
        return blocked
    else:
        return in_void


def day14_1(file):
    grid = parse_paths(file)

    pours = 0
    while not pour_sand(grid):
        pours += 1

    #display_grid(grid, offsetx=440)
    print(pours)


def day14_2(file):
    grid = parse_paths(file, add_floor=True)

    pours = 0
    while not pour_sand(grid, return_blocked=True):
        pours += 1

    #display_grid(grid, offsetx=460)
    print(pours + 1)


if __name__ == '__main__':
    day14_1(sys.argv[1])
    day14_2(sys.argv[1])

