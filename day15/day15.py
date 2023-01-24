#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/15
#

import sys
import re
import numpy as np

CELL_VOID = 0
CELL_BEACON = 1
CELL_SENSOR = 2
CELL_COVER = 3


def symbol(cell):
    cell_map = {CELL_VOID: '.', CELL_BEACON: 'B', CELL_SENSOR: 'S', CELL_COVER: '#'}
    return cell_map[cell]


def display_grid(grid):
    liney = 0
    for y in range(grid.shape[1]):
        print(''.join([symbol(grid[x][y]) for x in range(grid.shape[0])]), " <-" if liney == 10 else "")
        liney += 1


def manhattan_distance(s):
    return abs(s[1] - s[3]) + abs(s[0] - s[2])


def day15_1(file, line_no=10):
    sensors = []
    with open(file) as f:
        for line in f:
            if m := re.match(r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)',
                             line.strip()):
                sensors.append(tuple([int(x) for x in list(m.groups())]))

    min_x = min([s[0] - manhattan_distance(s) for s in sensors])
    max_x = max([s[0] + manhattan_distance(s) for s in sensors])
    size = max_x - min_x
    row = np.zeros((size,))

    for s in sensors:
        if s[1] == line_no:
            row[s[0] - min_x] = CELL_SENSOR
        if s[3] == line_no:
            row[s[2] - min_x] = CELL_BEACON

    for s in sensors:
        md = manhattan_distance(s)
        if s[1] - md <= line_no <= s[1] + md:
            sensor_to_line_no = abs(line_no - s[1])
            for x in range(s[0] - (md - sensor_to_line_no) - min_x,
                           s[0] + (md - sensor_to_line_no) - min_x + 1):
                if 0 <= x < row.shape[0]:
                    if row[x] == CELL_VOID:
                        row[x] = CELL_COVER

    #print(''.join([symbol(x) for x in row[-min_x:20-min_x+1]]))
    print(len([x for x in row if x == CELL_COVER]))


def day15_2(file):
    sensors = []
    with open(file) as f:
        for line in f:
            if m := re.match(r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)',
                             line.strip()):
                sensors.append(tuple([int(x) for x in list(m.groups())]))

        print(sum([(manhattan_distance(s)+2)*4 for s in sensors]))
        min_x = min([s[0] - manhattan_distance(s) for s in sensors])
        max_x = max([s[0] + manhattan_distance(s) for s in sensors])
        size_x = max_x - min_x
        min_y = min([s[1] - manhattan_distance(s) for s in sensors])
        max_y = max([s[1] + manhattan_distance(s) for s in sensors])
        size_y = max_y - min_y
        #print(sum([manhattan_distance(s) for s in sensors]))
        #print(size_x * size_y)


if __name__ == '__main__':
    day15_1(sys.argv[1], line_no=2_000_000)
    #day15_2(sys.argv[1])

