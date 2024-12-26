#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2024/day/7
#

import sys
import re


def increment_base3(base3_str):
    # Convert the base-3 string to a decimal integer
    decimal_number = int(base3_str, 3)
    # Increment the number
    incremented_number = decimal_number + 1
    # Convert the incremented number back to base-3
    base3_result = ''
    while incremented_number > 0:
        base3_result = str(incremented_number % 3) + base3_result
        incremented_number //= 3
    # Ensure the result has the same number of digits as the input
    base3_result = base3_result.zfill(len(base3_str))
    return base3_result or '0'


def parse_file(file):
    equations = []
    with open(file) as f:
        for line in f:
            line = line.strip()
            if m := re.search(r'^(\d+): (.*)$', line):
                equations.append({
                    'result': int(m.group(1)),
                    'numbers': [int(n) for n in m.group(2).split(' ')]
                })

    return equations


def eval_equation(equation):
    for i in range(2 ** (len(equation['numbers']) - 1)):
        # The variable i will be used to perform calculation with all the combinations of '+' and '*' given the
        # number of the equation numbers
        mask = 1
        equation_result = equation['numbers'][0]
        for n in range(1, len(equation['numbers'])):
            if i & mask:
                equation_result += equation['numbers'][n]
            else:
                equation_result *= equation['numbers'][n]
            mask <<= 1

        if equation_result == equation['result']:
            return True


def eval_equation_3ops(equation):
    # Initialize a base-3 representation as a string with zeros
    # The length is one less than the number of numbers in the equation
    it = "0" * (len(equation['numbers']) - 1)

    # Iterate through all possible combinations of the three operations (3^(number of numbers - 1))
    for i in range(3 ** (len(equation['numbers']) - 1)):
        # Start with the first number
        equation_result = equation['numbers'][0]

        # Apply operations based on the current base-3 representation
        for n in range(len(equation['numbers']) - 1):
            if it[n] == "0":  # Use addition for "0"
                equation_result += equation['numbers'][n + 1]
            elif it[n] == "1":  # Use multiplication for "1"
                equation_result *= equation['numbers'][n + 1]
            elif it[n] == "2":  # Concatenate numbers for "2"
                equation_result = int(str(equation_result) + str(equation['numbers'][n + 1]))

        # Increment the base-3 representation
        it = increment_base3(it)

        # Check if the resulting value matches the target result
        if equation_result == equation['result']:
            return True


def find_calibration_result(equations):
    calibration_result = 0

    for equation in equations:
        if eval_equation(equation):
            calibration_result += equation['result']

    return calibration_result


def find_calibration_result_3ops(equations):
    calibration_result = 0

    for equation in equations:
        if eval_equation_3ops(equation):
            calibration_result += equation['result']

    return calibration_result


def day7_1(file):
    equations = parse_file(file)
    print(find_calibration_result(equations))


def day7_2(file):
    equations = parse_file(file)
    print(find_calibration_result_3ops(equations))


if __name__ == '__main__':
    day7_1(sys.argv[1])
    day7_2(sys.argv[1])
