#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/1
#

import sys


def day1_1(file):
    with open(file, 'r') as f:
        print(max([sum(map(lambda x: int(x if x else 0), line.split("\n")))
                   for line in f.read().split("\n\n") if line]))


def day1_2(file):
    with open(file, 'r') as f:
        print(sum(sorted([sum(map(lambda x: int(x if x else 0), line.split("\n")))
                      for line in f.read().split("\n\n") if line])[-3:]))


if __name__ == '__main__':
    day1_1(sys.argv[1])
    day1_2(sys.argv[1])

