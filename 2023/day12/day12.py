#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/12
#

import sys
import re
import itertools
import fnmatch


def partitions(n, k):
    # Generate all partitions of n into k parts.

    # If the number of partition is just 1, simply return n
    if k == 1:
        yield [n]
        return

    # Generate all possible partitions of n
    parts = itertools.combinations(range(1, n), k - 1)

    # Create distinct partitions by taking differences between combinations
    for p in parts:
        partition = [p[0]]
        for i in range(1, len(p)):
            partition.append(p[i] - p[i - 1])
        partition.append(n - p[-1])
        yield partition


def partitions_with_zeroes(n, k):
    # Generate all partitions of n into k parts including the fact that the first and the last can be 0
    # The idea is to generate 4 sets of partitions:
    # partitions(n, k) : The first and last partitions will be greater than 0
    # partitions(n, k-1) with 0 at first : The first partition will be 0 and the last partitions greater than 0
    # partitions(n, k-1) with 0 at last : The first partition greater than 0 and the last partitions will be 0
    # partitions(n, k-1) with 0 at first and last : The first and last partitions will both be 0
    return list(partitions(n, k)) + list([[0] + p for p in partitions(n, k - 1)]) + \
           list([p + [0] for p in partitions(n, k - 1)]) + list([[0] + p + [0] for p in partitions(n, k - 2)])


def parse_file(file):
    records = []

    with open(file) as f:
        for line in f:
            # Match the line format and try to find the match in the line
            match = re.search(r"^(.+)\s+(.+)$", line.rstrip())

            if match:
                spring_groups = list(map(int, match.group(2).split(",")))
                records.append((match.group(1), spring_groups))

    return records


def find_matches(unknown_record, spring_groups):
    print(f"find_matches({unknown_record}, {spring_groups}")
    spring_sum = sum(spring_groups)
    nb_matches = 0

    # We try to find all possible combinations of springs and try to match them with the fnmatch function (witch
    # support the wildcard '?')
    # To generate all possible combinations, we consider the number of operational springs we could have between
    # each group of damaged springs. The total is the total springs - the damaged springs. And these operational
    # springs will be split into "damaged springs" + 1 groups. So we need to the partition the total of operational
    # springs and find all possible values. But we need to add one of more constraint: the first and the last
    # partitions can be 0, but the others cannot, because a group damaged springs can be at beginning or at the end,
    # and 2 groups of damaged springs must be separated by at least one operational spring.
    #
    # For instance:
    # ???..### 1,1,3
    #
    # Total springs is 8
    # We know that we have 1 + 1 + 3 = 5 damaged springs so the number of operational springs is 8 - 5 = 3
    # We have 3 groups of damaged springs, we need to split 3 into 4 groups and find all combinations considering the
    # constraint described above. These combinations are :
    #  [0, 1, 1, 1] , [1, 1, 1, 0], [0, 1, 2, 0], [0, 2, 1, 0]
    #
    # And with these list, we are able to generate all possible patterns of operational and damages springs:
    #  #.#.###.
    #  .#.#.###
    #  #.#..###
    #  #..#.###
    for p in partitions_with_zeroes(len(unknown_record) - spring_sum, len(spring_groups) + 1):
        pattern = ""
        for n in range(len(spring_groups)):
            pattern += "." * p[n]
            pattern += "#" * spring_groups[n]
        pattern += "." * p[-1]

        if fnmatch.fnmatch(pattern, unknown_record):
            nb_matches += 1

    print(unknown_record, spring_groups, nb_matches)
    return nb_matches


def find_matches_sum(records):
    return sum([find_matches(record[0], record[1]) for record in records])


def find_matches_sum_unfolded(records):
    return sum([find_matches(record[0] + "?", record[1]) for record in records])


def day12_1(file):
    print(find_matches_sum(parse_file(file)))


def day12_2(file):
    #print(find_matches_sum_unfolded(parse_file(file)))
    records = parse_file(file)
    for record in records:
        print("?".join([record[0]] * 5), record[1] * 5)

    #find_matches("????.#...#...?????", [4, 1, 1, 4])
    #find_matches("?????.#...#...", [4, 1, 1, 4])


if __name__ == '__main__':
    #day12_1(sys.argv[1])
    day12_2(sys.argv[1])

