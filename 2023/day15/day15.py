#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/15
#

import sys


def str2hash(string):
    current_hash = 0
    for ch in string:
        current_hash = ((current_hash + ord(ch)) * 17) % 256

    return current_hash


def parse_file(file):
    with open(file) as f:
        steps = f.readline().rstrip().split(',')

    return steps


def find_sum(steps):
    result = 0

    for step in steps:
        result += str2hash(step)

    return result


def day15_1(file):
    print(find_sum(parse_file(file)))


def day15_2(file):
    print(parse_file(file))


if __name__ == '__main__':
    day15_1(sys.argv[1])
    #day15_2(sys.argv[1])

