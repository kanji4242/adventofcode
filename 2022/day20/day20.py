#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/20
#

import sys


def read_sequence(file):
    with open(file) as f:
        sequence = list(enumerate([int(line.strip()) for line in f.readlines()]))

    return sequence


def move_in_list(sequence, index):
    indexes = [x[0] for x in sequence]
    old_index = indexes.index(index)
    # Since the list circular we need never place a number at the end of the list
    # That's why are applying modulo the size of the list - 1
    new_index = (old_index + sequence[old_index][1]) % (len(sequence) - 1)

    # Likewise if a number ends up at the beginning we place it at the of end list
    if new_index == 0:
        new_index = len(sequence) - 1

    # Pop the number and insert it at its new position
    sequence.insert(new_index, sequence.pop(old_index))


def get_grove_coordinates(sequence):
    index_zero = [x[1] for x in sequence].index(0)
    result = 0
    for index in [1000, 2000, 3000]:
        result += sequence[(index_zero + index) % len(sequence)][1]

    return result

def day20_1(file):
    sequence = read_sequence(file)

    for index in range(len(sequence)):
        move_in_list(sequence, index)

    print(get_grove_coordinates(sequence))


def day20_2(file):
    sequence = read_sequence(file)
    sequence = list(map(lambda x: (x[0], x[1] * 811589153), sequence))

    for x in range(10):
        for index in range(len(sequence)):
            move_in_list(sequence, index)

    print(get_grove_coordinates(sequence))


if __name__ == '__main__':
    day20_1(sys.argv[1])
    day20_2(sys.argv[1])
