#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/3
#

import sys
import numpy as np


def erase_symbol(ch):
    if not ch.isdigit() and ch != '.':
        return 's'
    else:
        return ch


def parse_number(schem, coord_x, coord_y):
    # Parse a number at a given coordinate search both forward AND backward
    number = ""

    if schem[coord_x, coord_y].isdigit():
        # Iterate over schematics looking forward
        x = coord_x
        while x < schem.shape[0] and schem[x, coord_y].isdigit():
            number += schem[x, coord_y]
            x += 1

        # Do the same but looking backward instead
        x = coord_x - 1
        while x >= 0 and schem[x, coord_y].isdigit():
            number = schem[x, coord_y] + number
            x -= 1

    # Returns 0 if no number has been found
    return int(number) if number else 0


def parse_schematic(file, with_erase_symbol=True):
    # First parse to find the size of the heightmap
    with open(file) as f:
        size_x, size_y = 0, 0

        for line in f:
            size_x = max(size_x, len(line.rstrip()))
            size_y += 1

    # Initialize the array
    schem = np.ndarray((size_x, size_y), dtype=object)

    # Second parse to fill the array
    with open(file) as f:
        y = 0
        for line in f:
            line = line.rstrip()
            if with_erase_symbol:
                schem[:, y] = [erase_symbol(ch) for ch in line]
            else:
                schem[:, y] = [ch for ch in line]

            y += 1

    return schem


def find_numbers(schem):
    result = 0

    for y in range(schem.shape[1]):
        x = 0
        while x < schem.shape[0]:
            # Find a digit in the schematics
            if schem[x, y].isdigit():
                part_number = False
                number = ""
                # If we have fonud a digit continue to iterate while we still have digits and did not cross the limit
                while x < schem.shape[0] and schem[x, y].isdigit():
                    number += schem[x, y]
                    # Search in the neighborhood the digit if a symbol is present
                    # If so, we consider the number we're parsing as a part number
                    if np.count_nonzero(schem[max(0, x - 1):x + 2, max(0, y - 1):y + 2] == 's') > 0:
                        part_number = True
                    x += 1

                if part_number:
                    # Add the number to the sum if this number is a part number
                    result += int(number)
            x += 1

    return result


def find_gears(schem):
    result = 0

    for y in range(schem.shape[1]):
        for x in range(schem.shape[0]):
            # Find a gear ('*' symbol)
            if schem[x, y] == '*':
                numbers = []
                # Search in the neighborhood the gear if we have digit and call the parse_number function
                # to get the number
                for coord in [
                    (x - 1, y - 1),
                    (x, y - 1),
                    (x + 1, y - 1),
                    (x + 1, y),
                    (x + 1, y + 1),
                    (x, y + 1),
                    (x - 1, y + 1),
                    (x - 1, y)
                ]:
                    numbers.append(parse_number(schem, coord[0], coord[1]))

                # We will have zero numbers meaning that there is no number at some coordinates, so delete them
                # We're also likely to parse the number several times because the number may reside on several
                # coordinates of the neighborhood. So we delete the duplicates
                numbers = list(set([nb for nb in numbers if nb]))

                # If we have exactly 2 numbers, we know that it's a gear, so we add it
                if len(numbers) == 2:
                    result += numbers[0] * numbers[1]

    return result


def day3_1(file):
    schem = parse_schematic(file)
    print(find_numbers(schem))


def day3_2(file):
    schem = parse_schematic(file, with_erase_symbol=False)
    print(find_gears(schem))


if __name__ == '__main__':
    day3_1(sys.argv[1])
    day3_2(sys.argv[1])

