#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/1
#

import sys


def day1(file):
    with open(file, 'r') as f:
        print(max([sum(map(lambda x: int(x), line.split("\n"))) for line in f.read().split("\n\n") if line]))


if __name__ == '__main__':
    day1(sys.argv[1])

