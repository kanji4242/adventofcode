#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2025/day/3
#

import sys


def find_highest(list_nb):
    list_nb = [ int(x) for x in list(list_nb) ]
    pivot = list_nb.index(max(list_nb))

    max_left = max(list_nb[:pivot]) if list_nb[:pivot] else 0
    max_right = max(list_nb[pivot + 1:]) if list_nb[pivot + 1:] else 0

    nb_left = max_left * 10 + list_nb[pivot] if max_left > 0 else 0
    nb_right = list_nb[pivot] * 10 +  max_right if max_right > 0 else 0

    return max(nb_left, nb_right)

def max_subsequence(list_nb, k):
    """
    Selects k digits from the list 'nums' to form the largest possible number,
    while preserving the original order of digits.
    This returns a subsequence (not necessarily consecutive elements).
    """
    list_nb = [int(x) for x in list(list_nb)]

    stack = []
    # Number of digits we are allowed to remove.
    # If list_nb has length N, and we keep k digits, we must remove N - k digits.
    to_remove = len(list_nb) - k

    for n in list_nb:
        # While the stack is not empty, we still have removals left and the last digit in
        # the stack is smaller than the current digit, then removing the last digit will allow
        # us to build a bigger number.
        while stack and to_remove > 0 and stack[-1] < n:
            # Remove the smaller digit
            stack.pop()
            # One removal used
            to_remove -= 1   

        # Add the current digit to the stack
        stack.append(n)

    # If we couldn't remove enough digits during the loop
    # (e.g. digits were in decreasing order), the stack will be too long.
    # We keep only the first k digits.
    return int("".join(map(str, stack[:k])))

def parse_file(file):
    result = 0
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            result += find_highest(line)

    return result

def parse_file2(file):
    result = 0
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            result += max_subsequence(line, 12)

    return result

def day3_1(file):
    print(parse_file(file))

def day3_2(file):
    print(parse_file2(file))
    #print(max_subsequence([ int(x) for x in list("818181911112111") ], 12))


if __name__ == '__main__':
    #day3_1(sys.argv[1])
    day3_2(sys.argv[1])

