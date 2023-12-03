#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/1
#

import sys


def scan_document(file, with_letters_digits=False):
    calibration_sum = 0
    letters_digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

    with open(file) as f:
        for line in f:
            line = line.rstrip()
            first_digit, last_digit = None, None

            if with_letters_digits:
                new_line = ""
                for ch in line:
                    new_line = new_line + ch
                    for digit, letters_digit in enumerate(letters_digits):
                        new_line = new_line.replace(letters_digit, f"{digit + 1}")

                new_line2 = line
                for digit, letters_digit in enumerate(letters_digits):
                    new_line2 = new_line2.replace(letters_digit, f"{digit + 1}")

                new_line3 = line
                i = 0
                while i < len(new_line3):
                    for digit, letters_digit in enumerate(letters_digits):
                        #print(i, new_line3[i:], letters_digit)
                        if new_line3[i:].startswith(letters_digit):
                            new_line3 = new_line3[:i] + f"{digit + 1}" + new_line3[i + len(letters_digit):]
                    i += 1

                print(line, new_line3)

                #if new_line != new_line2:
                #    print(line, new_line, new_line2)
                line = new_line3

            for ch in line:
                if ord('0') <= ord(ch) <= ord('9'):
                    if not first_digit:
                        first_digit = ch
                    last_digit = ch

            print(first_digit, last_digit)

            calibration_sum += int(first_digit + last_digit)

    print(calibration_sum)


def day1_1(file):
    scan_document(file)

def day1_2(file):
    scan_document(file, with_letters_digits=True)


if __name__ == '__main__':
    #day1_1(sys.argv[1])
    day1_2(sys.argv[1])

