#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/3
#

import sys
import string


def day3(file):
    priorities = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    sum_priorities = 0

    with open(file) as f:
        for line in f:
            rucksack1 = {x: True for x in line.rstrip()[:len(line) >> 1]}
            commmon_items = list(set([x for x in line.rstrip()[len(line) >> 1:] if x in rucksack1.keys()]))
            sum_priorities = sum_priorities + sum([priorities.index(x) + 1 for x in commmon_items])

    print(sum_priorities)


if __name__ == '__main__':
    day3(sys.argv[1])