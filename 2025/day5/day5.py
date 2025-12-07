#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2025/day/5
#

import sys


def merge_ranges(ranges):
    # Ranges needs to be sorted by starting interval
    ranges.sort()

    merged = []
    start, end = ranges[0]

    for s, e in ranges[1:]:

        if s <= end:  # overlap
            end = max(end, e)

        else:  # no overlap, then push previous and start new
            merged.append((start, end))
            start, end = s, e

    merged.append((start, end))

    return merged

def parse_file(file):
    fresh_ranges = []
    available_ingredients = []

    with open(file) as f:
        for line in f:
            if '-' in line:
                begin, end = line.rstrip().split('-')
                fresh_ranges.append((int(begin), int(end)))
            elif line.rstrip().isdigit():
                available_ingredients.append(int(line))

    return fresh_ranges, available_ingredients

def get_nb_fresh_ingredients(file):
    fresh_ranges, available_ingredients = parse_file(file)
    fresh_ingredients = []

    for ingredient_id in available_ingredients:
        for fresh_range in fresh_ranges:
            if fresh_range[0] <= ingredient_id <= fresh_range[1]:
                fresh_ingredients.append(ingredient_id)

    return len(set(fresh_ingredients))

def get_nb_all_fresh_ingredients(file):
    fresh_ranges, available_ingredients = parse_file(file)
    return sum(e - s + 1 for s, e in merge_ranges(fresh_ranges))

def day5_1(file):
    print(get_nb_fresh_ingredients(file))

def day5_2(file):
    print(get_nb_all_fresh_ingredients(file))


if __name__ == '__main__':
    day5_1(sys.argv[1])
    day5_2(sys.argv[1])

