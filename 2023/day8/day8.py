#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/8
#

import sys
import re


class Node(tuple):
    """
    Node subclass tuple with 2 values left and right
    It adds .left and .right properties for more code clarity
    """

    def __new__(cls, x=0, y=0):
        return super(Node, cls).__new__(cls, tuple((x, y)))

    @property
    def left(self):
        return self[0]

    @property
    def right(self):
        return self[1]


def parse_file(file):
    nodes = {}
    with open(file) as f:
        instructions = [c for c in f.readline().rstrip()]

        for line in f:
            line = line.rstrip()

            # Match the line format and try to find the match in the line
            match = re.search(r"(\w+) = \((\w+),\s*(\w+)\)", line)

            if match:
                nodes[match.group(1)] = Node(match.group(2), match.group(3))

    print(instructions, nodes)

    return instructions, nodes


def lookup_nodes(instructions, nodes):
    instruction_index = 0
    current_node = 'AAA'
    nb_steps = 0

    while current_node != 'ZZZ':
        print(f"instruction: {instructions[instruction_index]}")
        if instructions[instruction_index] == 'L':
            current_node = nodes[current_node].left
        elif instructions[instruction_index] == 'R':
            current_node = nodes[current_node].right
        else:
            print(f"Unknown instruction: {instructions[instruction_index]}")

        print(f"current node: {current_node}")
        instruction_index = (instruction_index + 1) % len(instructions)
        nb_steps += 1

    return nb_steps


def day8_1(file):
    instructions, nodes = parse_file(file)
    print(lookup_nodes(instructions, nodes))


def day8_2(file):
    print(parse_file(file))


if __name__ == '__main__':
    day8_1(sys.argv[1])
    #day8_2(sys.argv[1])

