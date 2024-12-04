#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2024/day/2
#

import sys
import re


def is_monotonic(values):
    is_increasing = all(values[i] < values[i + 1] for i in range(len(values) - 1))
    is_decreasing = all(values[i] > values[i + 1] for i in range(len(values) - 1))
    return is_increasing or is_decreasing


def are_adjacent_differences_valid(values):
    return all(1 <= abs(values[i] - values[i + 1]) <= 3 for i in range(len(values) - 1))


def parse_file(file):
    with open(file) as f:
        lines = []
        for line in f:
            lines.append(list(map(int, re.split(r' +', line.strip()))))

    return lines


def print_safe_list_nb(file):
    lines = parse_file(file)
    safe_lists = 0

    for values in lines:
        if is_monotonic(values) and are_adjacent_differences_valid(values):
            safe_lists += 1

    print(safe_lists)


def print_safe_list_with_toleration(file):
    lines = parse_file(file)
    safe_lists = 0

    for values in lines:
        if is_monotonic(values) and are_adjacent_differences_valid(values):
            safe_lists += 1
        else:
            for i in range(len(values)):
                new_values = values[:]
                new_values.pop(i)
                print(values, new_values)
                if is_monotonic(new_values) and are_adjacent_differences_valid(new_values):
                    safe_lists += 1
                    break

    print(safe_lists)


def day2_1(file):
    print_safe_list_nb(file)


def day2_2(file):
    print_safe_list_with_toleration(file)


if __name__ == '__main__':
    day2_1(sys.argv[1])
    day2_2(sys.argv[1])

