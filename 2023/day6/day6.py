#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/6
#

import sys
import re
import math


def parse_races(file):
    with open(file) as f:
        line = f.readline().rstrip()
        match = re.search(r"Time:\s+(.+)", line)

        times = list(map(int, re.split(r"\s+", match.group(1))))

        line = f.readline().rstrip()
        match = re.search(r"Distance:\s+(.+)", line)

        distances = list(map(int, re.split(r"\s+", match.group(1))))

    return list(zip(times, distances))


def find_nb_ways_for_records(races):
    result = 1
    for race in races:
        nb_ways = 0
        race_time = race[0]
        race_distance = race[1]

        # Iterate over every possibility form holding the button for 0 milliseconds up to the number of milliseconds
        # the race has last
        for n in range(race_time + 1):
            if n * (race_time - n) > race_distance:
                nb_ways += 1

        result = result * nb_ways

    return result


def find_nb_ways_for_records2(races):
    race_time = int(''.join([str(r[0]) for r in races]))
    race_distance = int(''.join([str(r[1]) for r in races]))

    # We cannot proceed by iteration on this. But we can notice that the formula n * (race_time - n) used in
    # the previous method is in fact a quadratic equation. We can solve this equation and get 2 roots.
    # The number of ways will be between these 2 roots.
    #
    # To get the equation, we follow these steps:
    # n * (race_time - n) == race_distance
    # n * race_time - n ** 2 == race_distance
    # - n ** 2 + n * race_time - race_distance == 0
    #
    # So we now have quadratic equation with the following coefficients:
    # a = -1, b = race_time, c = - race_distance

    # We then calculate the delta
    delta = race_time**2 - 4 * race_distance

    # And we now get the 2 roots, the first one will be the minimum of milliseconds to beat the record, and the
    # second one will be the maximum of milliseconds
    min_range = math.floor(-(- race_time + math.sqrt(delta)) / 2) + 1
    max_range = math.floor(-(- race_time - math.sqrt(delta)) / 2)

    # We return the delta between these 2 values
    return max_range - min_range + 1


def day6_1(file):
    print(find_nb_ways_for_records(parse_races(file)))


def day6_2(file):
    print(find_nb_ways_for_records2(parse_races(file)))


if __name__ == '__main__':
    day6_1(sys.argv[1])
    day6_2(sys.argv[1])

