#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/25
#

import sys


def parse_snafus(file):
    snafus = []
    with open(file) as f:
        for line in f:
            snafus.append(line.strip())

    return snafus


def snafu2int(snafu):
    digits = {"0": 0, "1": 1, "2": 2, "=": -2, "-": -1}
    snafu_digits = [digits[d] for d in snafu]

    for x in range(len(snafu_digits) - 1, 0, -1):
        if snafu_digits[x] < 0:
            snafu_digits[x] += 5
            snafu_digits[x - 1] -= 1

    return int(''.join([str(d) for d in snafu_digits]), 5)


def int2snafu(nb):
    digits = {0: "0", 1: "1", 2: "2", -2: "=", -1: "-"}
    nb_digits = []

    while nb > 0:
        nb, r = divmod(nb, 5)
        nb_digits.insert(0, r)

    for x in range(len(nb_digits) - 1, 0, -1):
        if nb_digits[x] > 2:
            nb_digits[x] -= 5
            nb_digits[x - 1] += 1

    if nb_digits[0] > 2:
        nb_digits[0] -= 5
        nb_digits.insert(0, 1)

    return ''.join([digits[d] for d in nb_digits])


def day25_1(file):
    snafus = parse_snafus(file)
    print(int2snafu(sum([snafu2int(x) for x in snafus])))


def day25_2(file):
    # To be continued (don't have enough stars)
    pass


if __name__ == '__main__':
    day25_1(sys.argv[1])
    day25_2(sys.argv[1])
