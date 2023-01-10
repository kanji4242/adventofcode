#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/13
#

import sys
import functools


def compare(value1, value2):
    if type(value1) is int and type(value2) is int:
        return (value1 > value2) - (value1 < value2)

    elif type(value1) is list and type(value2) is list:
        for x, y in zip(value1, value2):
            if ret := compare(x, y):
                return ret
        if len(value2) != len(value1):
            return (len(value1) > len(value2)) - (len(value1) < len(value2))

    elif type(value1) is int and type(value2) is list:
        return compare([value1], value2)

    elif type(value1) is list and type(value2) is int:
        return compare(value1, [value2])

    return 0


def day13_1(file):
    with open(file) as f:
        sum_indexes = 0
        index = 1
        packet1 = packet2 = None

        for line in f:
            if not line.strip():
                continue
            if packet1 is None:
                packet1 = eval(line)
            elif packet2 is None:
                packet2 = eval(line)
                if compare(packet1, packet2) == -1:
                    sum_indexes += index

                packet1 = packet2 = None
                index += 1

    print(sum_indexes)


def day13_2(file):
    with open(file) as f:
        packets = []
        for line in f:
            if line.strip():
                packets.append(eval(line.strip()))
    packets = sorted(packets, key=functools.cmp_to_key(compare))

    divisors = [[[2]], [[6]]]
    offset_divisor = 0
    decoder_key = 1

    for index in range(len(packets)):
        packet = packets[index]
        if compare(packet, divisors[offset_divisor]) > 0:
            decoder_key *= index + offset_divisor + 1
            offset_divisor += 1

        if offset_divisor >= len(divisors):
            break

    print(decoder_key)


if __name__ == '__main__':
    day13_1(sys.argv[1])
    day13_2(sys.argv[1])
