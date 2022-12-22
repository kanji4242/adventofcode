#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/6
#

import sys


def start_of_packet(datastream):
    for n in range(len(datastream)):
        if len(datastream[n:n + 4]) == 4 and len(set(datastream[n:n + 4])) == 4:
            n += 4
            break
    return n


def start_of_message(datastream):
    for n in range(len(datastream)):
        if len(datastream[n:n + 14]) == 14 and len(set(datastream[n:n + 14])) == 14:
            n += 14
            break
    return n


def day6_1(file):
    with open(file) as f:
        for line in f:
            print(start_of_packet(line.strip()))


def day6_2(file):
    with open(file) as f:
        for line in f:
            print(start_of_message(line.strip()))


if __name__ == '__main__':
    day6_1(sys.argv[1])
    day6_2(sys.argv[1])

