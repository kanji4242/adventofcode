#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/9
#

import sys
import numpy as np


def display_grid(knots_pos):
    xmin = min([x[0] for x in knots_pos])
    xmax = max([x[0] for x in knots_pos])
    ymin = min([x[1] for x in knots_pos])
    ymax = max([x[1] for x in knots_pos])

    grid = np.full((xmax - xmin + 1, ymax - ymin + 1), ".", dtype=str)
    print(grid.shape, xmin, xmax, ymin, ymax)
    for n, pos in reversed(list(enumerate(knots_pos))):
        print(pos[0], pos[1], pos[0] - xmin, pos[1] - ymin)
        grid[pos[0] - xmin][pos[1] - ymin] = str(n)

    print(grid)


def move_head(command, head_pos):
    if command.startswith("R"):
        head_pos[0] += 1
    elif command.startswith("D"):
        head_pos[1] -= 1
    elif command.startswith("U"):
        head_pos[1] += 1
    elif command.startswith("L"):
        head_pos[0] -= 1

    return head_pos[0], head_pos[1]


def move_tail(head_pos, tail_pos):
    delta_x = head_pos[0] - tail_pos[0]
    delta_y = head_pos[1] - tail_pos[1]

    if delta_x == 2 or delta_x == -2:
        tail_pos[0] += delta_x >> 1
        if delta_y == 1 or delta_y == -1:
            tail_pos[1] += delta_y

    if delta_y == 2 or delta_y == -2:
        tail_pos[1] += delta_y >> 1
        if delta_x == 1 or delta_x == -1:
            tail_pos[0] += delta_x

    return tail_pos[0], tail_pos[1]


def day9_1(file):
    head_pos = [0, 0]
    tail_pos = [0, 0]
    visited_positions = []
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            steps = int(line.split(" ")[1])
            for _ in range(steps):
                head_pos[0], head_pos[1] = move_head(line, head_pos)
                tail_pos[0], tail_pos[1] = move_tail(head_pos, tail_pos)
                visited_positions.append(tuple(tail_pos))

    print(len(set(visited_positions)))


def day9_2(file):
    knots_pos = []
    for _ in range(10):
        knots_pos.append([0, 0])

    visited_positions = []
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            steps = int(line.split(" ")[1])
            for _ in range(steps):
                knots_pos[0][0], knots_pos[0][1] = move_head(line, knots_pos[0])
                for i in range(1, len(knots_pos)):
                    knots_pos[i][0], knots_pos[i][1] = move_tail(knots_pos[i - 1], knots_pos[i])
                    if i == 9:
                        visited_positions.append(tuple(knots_pos[i]))

            #display_grid(knots_pos)
    print(len(set(visited_positions)))


if __name__ == '__main__':
    day9_1(sys.argv[1])
    day9_2(sys.argv[1])

