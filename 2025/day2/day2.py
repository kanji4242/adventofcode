#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2025/day/2
#

import sys

def is_valid(nb):
    str_nb = str(nb)
    if len(str_nb) % 2 == 1:
        return False
    else:
        return str_nb[:len(str_nb) // 2] == str_nb[len(str_nb)  // 2:]

def is_valid2(nb):
    str_nb = str(nb)
    if len(str_nb) >= 2:
        for part in range(2, len(str_nb) + 1):
            if len(str_nb) % part == 0:
                str_compare = str_nb[:len(str_nb) // part] * part
                if str_nb == str_compare:
                    return True
        return False
    else:
        return False


def parse_input(file, is_valid_funct):
    response = 0
    with open(file) as f:
        ranges = f.readline().rstrip()

        for rg in ranges.split(","):
            rg_start, rg_end = rg.split("-")
            for n in range(int(rg_start), int(rg_end) + 1):
                if is_valid_funct(n):
                    response += n

    return response

def day2_1(file):
    print(parse_input(file, is_valid))

def day2_2(file):
    print(parse_input(file, is_valid2))


if __name__ == '__main__':
    #day2_1(sys.argv[1])
    day2_2(sys.argv[1])

