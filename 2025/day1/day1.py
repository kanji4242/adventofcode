#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2025/day/1
#

import sys

def rotate_dial(file):
    dial_value = 50
    password = 0

    with open(file) as f:
        for line in f:
            if line[0] == "L":
                tick_number = int(line[1:])
                dial_value = (dial_value - tick_number) % 100
            elif line[0] == "R":
                tick_number = int(line[1:])
                dial_value = (dial_value + tick_number) % 100

            if dial_value == 0:
                password = password + 1

    return password

def rotate_dial2(file):
    dial_value = 50
    password = 0

    with open(file) as f:
        for line in f:
            tick_number = int(line[1:])

            if line[0] == "L":
                pace = -1
            elif line[0] == "R":
                pace = 1

            for n in range(tick_number):
                dial_value = (dial_value + pace) % 100
                if dial_value == 0:
                    password = password + 1

    return password

def day1_1(file):
    print(rotate_dial(file))

def day1_2(file):
    print(rotate_dial2(file))


if __name__ == '__main__':
    day1_1(sys.argv[1])
    day1_2(sys.argv[1])

