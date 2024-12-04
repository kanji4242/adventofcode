#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2024/day/1
#

import sys
import re


def parse_file(file):
    with open(file) as f:
        left_values = []
        right_values = []

        for line in f:
            if values := re.split(r' +', line.strip()):
                left_values.append(int(values[0]))
                right_values.append(int(values[1]))

    return left_values, right_values


def print_sum(file):
    left_values, right_values = parse_file(file)
    left_values = sorted(left_values)
    right_values = sorted(right_values)

    print(sum([abs(right_values[i] - left_values[i]) for i in range(len(left_values))]))


def print_similarity_score(file):
    left_values, right_values = parse_file(file)

    print(sum([left_values[i] * right_values.count(left_values[i]) for i in range(len(left_values))]))


def day1_1(file):
    print_sum(file)


def day1_2(file):
    print_similarity_score(file)


if __name__ == '__main__':
    day1_1(sys.argv[1])
    day1_2(sys.argv[1])

