#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/3
#

import sys
import string


def day3_1(file):
    priorities = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    sum_priorities = 0

    with open(file) as f:
        for line in f:
            commmon_items = list(set(line.rstrip()[:len(line) >> 1]) & set(line.rstrip()[len(line) >> 1:]))
            sum_priorities = sum_priorities + sum([priorities.index(x) + 1 for x in commmon_items])

    print(sum_priorities)


def day3_2(file):
    priorities = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    three_rucksacks = []
    sum_priorities = 0

    with open(file) as f:
        for line in f:
            three_rucksacks.append(line.rstrip())
            if len(three_rucksacks) == 3:
                commmon_items = list(set(three_rucksacks[0]) & set(three_rucksacks[1]) & set(three_rucksacks[2]))
                sum_priorities = sum_priorities + sum([priorities.index(x) + 1 for x in commmon_items])
                three_rucksacks = []

    print(sum_priorities)


if __name__ == '__main__':
    day3_1(sys.argv[1])
    day3_2(sys.argv[1])
