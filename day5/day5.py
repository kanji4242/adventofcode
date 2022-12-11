#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/5
#

import sys


def day5(file):
    stacks = [[]]
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            if line.find("[") >= 0:
                crates = [(cr[0], cr[1][1]) for cr in enumerate([line[st:st + 4] for st in range(0, len(line), 4)])
                          if cr[1][0:1] == '[' and cr[1][2:3] == ']']
                for crate in crates:
                    stacks.extend([list() for _ in range(len(stacks) - 1, crate[0])])
                    stacks[crate[0]].insert(0, crate[1])

            elif line.startswith("move "):
                for _ in range(int(line[5:line.find(" from ")])):
                    stacks[int(line[line.find(" to ") + 4:]) - 1].append(
                        stacks[int(line[line.find(" from ") + 6:line.find(" to ")]) - 1].pop())

        for i in range(max([len(st) for st in stacks]) - 1, -1, -1):
            print("".join([f"[{stack[i]}] " if i < len(stack) else " "*4 for stack in stacks]))

        print("".join([f"{i + 1:-2d}  " for i in range(len(stacks))]))


if __name__ == '__main__':
    day5(sys.argv[1])

