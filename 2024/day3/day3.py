#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2024/day/3
#

import sys
import re


def parse_file(file):
    with open(file) as f:
        string = "".join(f.readlines())

    # Find all occurrences of the pattern `mul(x, y)` in the substring,
    # where x and y are integers up to 3 digits long.
    muls = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', string)

    # Calculate the product of each pair of x and y
    print(sum([int(mul[0]) * int(mul[1]) for mul in muls]))


def parse_file_with_disable_enable(file):
    with open(file) as f:
        string = "".join(l.rstrip() for l in f)

    # Find all occurrences of the pattern `don't()` in the input string
    # and record their start indices along with the label 'dont'.
    sdont = [('dont', m.start()) for m in re.finditer(r"""don\'t\(\)""", string)]

    # Find all occurrences of the pattern `do()` in the input string
    # and record their start indices along with the label 'do'.
    sdo = [('do', m.start()) for m in re.finditer(r"""do\(\)""", string)]

    # Combine the found 'do' and 'dont' positions into a single list,
    # adding a 'do' at the start (index 0) and a 'dont' at the end (string length).
    # Sort this combined list based on the position of each item in the string.
    sdont_sdo = sorted(
        [('do', 0)] + sdont + sdo + [('dont', len(string))],
        key=lambda x: x[1]
    )

    result = 0

    # Iterate over the combined list, processing sections of the string
    # between each 'do' and the next 'dont'.
    for n in range(len(sdont_sdo) - 1):
        # Only process sections starting with 'do'
        if sdont_sdo[n][0] == 'do':
            # Extract the substring between the current 'do' and the next 'dont' or 'do'.
            substring = string[sdont_sdo[n][1]:sdont_sdo[n + 1][1]]

            # Find all occurrences of the pattern `mul(x, y)` in the substring,
            # where x and y are integers up to 3 digits long.
            muls = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', substring)

            # For each match, calculate the product of x and y, and add it to the result.
            result += sum([int(mul[0]) * int(mul[1]) for mul in muls])

    print(result)


def day3_1(file):
    parse_file(file)


def day3_2(file):
    parse_file_with_disable_enable(file)


if __name__ == '__main__':
    day3_1(sys.argv[1])
    day3_2(sys.argv[1])

