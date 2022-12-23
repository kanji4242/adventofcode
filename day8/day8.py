#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/8
#

import sys
import numpy as np


def parse_input(file):
    grid = None
    with open(file) as f:
        n = 0
        for line in f:
            line = line.rstrip()
            if grid is None:
                grid = np.zeros((len(line), len(line)), dtype=int)
            if n < len(line):
                grid[n] = list([int(x) for x in line])
            n += 1

    return grid


def scan_visible(line_or_col, visible_datas):
    max_height_left = max_height_right = -1
    for i in range(len(line_or_col)):
        if line_or_col[i] > max_height_left:
            max_height_left = line_or_col[i]
            visible_datas[i] = 1

        if line_or_col[len(line_or_col) - i - 1] > max_height_right:
            max_height_right = line_or_col[len(line_or_col) - i - 1]
            visible_datas[len(line_or_col) - i - 1] = 1


def get_scenic_score(line_or_col, index):
    print(line_or_col, index, line_or_col[index])
    max_height_left = max_height_right = -1
    view_left = view_right = 0
    for i in range(index - 1, -1, -1):
        if line_or_col[i] >= max_height_left and line_or_col[i] <= line_or_col[index]:
            max_height_left = line_or_col[i]
            view_left += 1

    for i in range(index + 1, len(line_or_col)):
        if line_or_col[i] >= max_height_right and line_or_col[i] <= line_or_col[index]:
            max_height_right = line_or_col[i]
            view_right += 1

    print(view_left, view_right)
    return view_left * view_right


def day8_1(file):
    grid = parse_input(file)
    visible_trees = np.zeros(grid.shape, dtype=int)
    for n in range(grid.shape[0]):
        scan_visible(grid[n], visible_trees[n])
        scan_visible(grid[:, n], visible_trees[:, n])
    print(grid)
    print(visible_trees)
    print(np.count_nonzero(visible_trees == 1))


def day8_2(file):
    grid = parse_input(file)
    scenic_scores = []
    for x in range(grid.shape[0]):
        for y in range(grid.shape[0]):
            score = get_scenic_score(grid[:, x], y) * get_scenic_score(grid[y], x)
            print("---", x, y, score)
            scenic_scores.append(score)
    print(max(scenic_scores))



if __name__ == '__main__':
    #day8_1(sys.argv[1])
    day8_2(sys.argv[1])

