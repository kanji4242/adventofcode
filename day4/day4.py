#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/4
#

import sys


def day4(file):
    contained_pairs = 0

    with open(file) as f:
        for line in f:
            pair1_start, pair1_end, pair2_start, pair2_end =\
                [int(x) for p in line.rstrip().split(',') for x in p.split('-')]

            if pair1_start > pair2_start:
                pair2_start, pair1_start = pair1_start, pair2_start
                pair2_end, pair1_end = pair1_end, pair2_end

            if pair1_start <= pair2_start and pair1_end >= pair2_end:
                contained_pairs += 1

    print(contained_pairs)


if __name__ == '__main__':
    day4(sys.argv[1])
