#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/9
#

import sys
import re


def parse_report(file):
    report = []
    with open(file) as f:
        for line in f:
            report.append([int(v) for v in re.split(r'\s+', line.strip())])

    return report


def find_extrapolated_value(values, backward_mode=False):
    # We just focus the last value from each difference iteration.
    # This is the only value we need to compute the extrapolated value.
    last_values = []

    # Start with the current values as the given list of values.
    current_values = values

    # For the part 1, since we're looking forward, we need to add the last value of the current values list
    # to the last_values list. For part 2, it will be the other way around, we're backward so we need to add
    # the first value instead.
    last_values.append(current_values[-1 if not backward_mode else 0])

    # Continue the loop until all values in the current values list are the same.
    # If this condition is true, this means that we have the seme difference for each number, which will
    # inevitably lead to a 0 difference on the next iteration, this is the stop condition
    # But we don't need to go further to this last step and stop immediately as this is now necessary for
    # computing the extrapolated value.
    while len(set(current_values)) > 1:
        # Compute the differences between adjacent values and store them in next_values list.
        current_values = [current_values[n + 1] - current_values[n] for n in range(len(current_values) - 1)]

        # Populate the last_values list in the same way we did just before the while loop
        last_values.append(current_values[-1 if not backward_mode else 0])

    extrapolated_value = 0

    # Sum up the values in the last values in reverse order.
    if not backward_mode:
        for last_value in reversed(last_values):
            extrapolated_value += last_value
    else:
        extrapolated_value = last_values[-1]
        for last_value in list(reversed(last_values))[1:]:
            extrapolated_value = last_value - extrapolated_value

    # Return the computed extrapolated value.
    return extrapolated_value


def day9_1(file):
    report = parse_report(file)
    extrapolated_values = 0
    for values in report:
        extrapolated_values += find_extrapolated_value(values)

    print(extrapolated_values)


def day9_2(file):
    report = parse_report(file)
    extrapolated_values = 0
    for values in report:
        extrapolated_values += find_extrapolated_value(values, backward_mode=True)

    print(extrapolated_values)


if __name__ == '__main__':
    day9_1(sys.argv[1])
    day9_2(sys.argv[1])

