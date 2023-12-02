#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/2
#

# 0 defeats 2
# 2 defeats 1
# 1 defeats 0



import sys


def day2_1(file):
    codes_opponent, codes_you = list("ABC"), list("XYZ")
    score = 0

    with open(file) as f:
        for line in f:
            opponent, you = line.rstrip().split(" ")
            score = score + codes_you.index(you) + 1
            # Draw
            if codes_you.index(you) == codes_opponent.index(opponent):
                score += 3
            # You won
            elif (codes_opponent.index(opponent) + 1) % 3 == codes_you.index(you):
                score += 6

    print(score)


def day2_2(file):
    codes_opponent, codes_strategy = list("ABC"), list("XYZ")
    score = 0

    with open(file) as f:
        for line in f:
            opponent, strategy = line.rstrip().split(" ")
            # You need to lose
            if strategy == "X":
                score += (codes_opponent.index(opponent) + 2) % 3 + 1
            # You need to end the round in a draw
            elif strategy == "Y":
                score += codes_opponent.index(opponent) + 4
            # You need to win
            elif strategy == "Z":
                score += (codes_opponent.index(opponent) + 1) % 3 + 7

    print(score)


if __name__ == '__main__':
    day2_1(sys.argv[1])
    day2_2(sys.argv[1])

