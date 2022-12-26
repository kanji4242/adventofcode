#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/10
#

import sys
import numpy as np


def draw_pixel(crt, cycle, register):
    if register - 1 <= ((cycle - 1) % 40) <= register + 1:
        crt[int((cycle - 1) / 40) % (40 * 6)][(cycle - 1) % 40] = 1


def day10_1(file):
    cycle_steps = list(range(20, 221, 40))
    cycle = 0
    register = 1
    signal_strength = 0
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            cycle_p = cycle
            register_p = register
            if line == "noop":
                cycle += 1
            elif line.startswith("addx"):
                register += int(line.split(" ")[1])
                cycle += 2

            for cs in cycle_steps:
                if cycle_p < cs <= cycle:
                    signal_strength += cs * register_p

    print(signal_strength)


def day10_2(file):
    cycle = 0
    register = 1
    crt = np.zeros((6, 40), dtype=int)

    with open(file) as f:
        for line in f:
            line = line.rstrip()
            if line == "noop":
                cycle += 1
                draw_pixel(crt, cycle, register)
            elif line.startswith("addx"):
                for _ in range(2):
                    cycle += 1
                    draw_pixel(crt, cycle, register)
                register += int(line.split(" ")[1])

    for y in range(crt.shape[0]):
        print("".join(["#" if x else "." for x in crt[y]]))


if __name__ == '__main__':
    day10_1(sys.argv[1])
    day10_2(sys.argv[1])

