#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2025/day/6
#

import sys
import re
import math

def parse_file(file):
    all_numbers = []
    operators = []
    len_numbers, len_operators = 0, 0

    with open(file) as f:
        for line in f:
            if '+' in line or '*' in line:
                operators = re.split(r' +', line.strip())
                len_operators = len(operators)
            elif line.strip():
                numbers = [int(x) for x in re.split(r' +', line.strip())]
                len_numbers = len(numbers)
                all_numbers.append(numbers)

    if len_numbers == len_operators:
        return all_numbers, operators
    else:
        return None, None

def parse_file2(file):
    cols = []
    all_numbers = []

    with open(file) as f:
        lines = []

        for line in f:
            if '+' in line or '*' in line:
                operators = re.split(r' +', line.strip())
            else:
                lines.append(line.rstrip('\n'))

        current_col = 0
        cols = []

        # Determine column boundaries by scanning character positions
        # We assume all lines have the same length as lines[0]
        for i in range(len(lines[0])):

            # Check if this character position is a separator (column break)
            is_separator = True
            for line in lines:
                if line[i] != ' ':
                    is_separator = False
                    break

            # If all lines have a space here, we found a column boundary
            if is_separator:
                # Save the start and end indices
                cols.append((current_col, i))
                # Next column starts after this space
                current_col = i + 1

        # Add final column (after the last separator)
        cols.append((current_col, len(lines[0])))

    # Re-open the file to extract the actual field values
    with open(file) as f:
        for line in f:
            if not('+' in line or '*' in line):
                # Extract each field by slicing the line using the column boundaries
                fields = [line[start:end] for start, end in cols]
                all_numbers.append(fields)

    return all_numbers, operators


def compute_grand_total(all_numbers, operators):
    grand_total = 0
    for n in range(len(operators)):
        # Extract the n‑th column from each row of all_numbers
        numbers = [an[n] for an in all_numbers]

        # Apply operator (+ or *) to the reconstructed numbers
        if operators[n] == '+':
            grand_total += sum(numbers)
        elif operators[n] == '*':
            grand_total += math.prod(numbers)

    return grand_total

def compute_grand_total_ltr_in_c(all_numbers, operators):
    grand_total = 0
    for n in range(len(operators)):
        # Extract the n‑th column from each row of all_numbers
        # 'numbers' becomes a list of strings (one string per row)
        numbers = [an[n] for an in all_numbers]

        # Reconstruct full numbers vertically:
        # numbers = [
        #   ['1','2','3'],   # row 1
        #   ['4','5','6'],   # row 2
        # ]
        # → we rebuild column-wise: "14", "25", "36"
        numbers2 = [int(''.join([number[i] for number in numbers])) for i in range(len(numbers[0]))]

        # Apply operator (+ or *) to the reconstructed numbers
        if operators[n] == '+':
            grand_total += sum(numbers2)
        elif operators[n] == '*':
            grand_total += math.prod(numbers2)

    return grand_total

def day6_1(file):
    all_numbers, operators = parse_file(file)
    print(compute_grand_total(all_numbers, operators))

def day6_2(file):
    all_numbers, operators = parse_file2(file)
    print(compute_grand_total_ltr_in_c(all_numbers, operators))

if __name__ == '__main__':
    day6_1(sys.argv[1])
    day6_2(sys.argv[1])

