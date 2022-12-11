#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/2
#

import sys


def day2(file):
    labels_opponent, labels_you = list("ABC"), list("XYZ")
    score = 0

    with open(file) as f:
        for line in f:
            opponent, you = line.rstrip().split(" ")
            score = score + labels_you.index(you) + 1
            if labels_opponent.index(opponent) == labels_you.index(you):
                score += 3
            elif (labels_you.index(you) + 1) % 3 == labels_opponent.index(opponent):
                score += 6

    print(score)


if __name__ == '__main__':
    day2(sys.argv[1])
