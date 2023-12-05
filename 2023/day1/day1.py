#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/1
#

import sys


def convert_letters_digits(line):
    # If you look at the lines you can see that some numbers overlap by one character. My trick is to replace
    # each number spelt out by the number written in figures but surrounded by its first and last characters.
    letters_digits = {
        'one': "o1e",
        'two': "t2o",
        'three': "t3e",
        'four': "f4r",
        'five': "f5e",
        'six': "s6x",
        'seven': "s7n",
        'eight': "e8t",
        'nine': "n9e"
    }
    new_line = line

    for letters_digit, replacement in letters_digits.items():
        new_line = new_line.replace(letters_digit, replacement)

    return new_line


def find_calibration_sum(file, with_letters_digits=False):
    calibration_sum = 0

    with open(file) as f:
        for line in f:
            line = line.rstrip()
            first_digit, last_digit = None, None

            if with_letters_digits:
                line = convert_letters_digits(line)

            for ch in line:
                if ord('0') < ord(ch) <= ord('9'):
                    if not first_digit:
                        first_digit = ch
                    last_digit = ch

            calibration_sum += int(first_digit + last_digit)

    return calibration_sum


def day1_1(file):
    print(find_calibration_sum(file))


def day1_2(file):
    print(find_calibration_sum(file, with_letters_digits=True))


if __name__ == '__main__':
    day1_1(sys.argv[1])
    day1_2(sys.argv[1])

