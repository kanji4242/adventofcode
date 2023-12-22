#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/8
#

import sys
import re
import math


def lcm(x, y):
    # Compute the Least Common Multiple (LCM) of two numbers
    return abs(x * y) // math.gcd(x, y)


def lcm_of_list(numbers):
    # Compute the LCM of numbers in a list
    if not numbers:
        return None
    result = numbers[0]
    for num in numbers[1:]:
        result = lcm(result, num)
    return result


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

    return instructions, nodes


def lookup_nodes(instructions, nodes, starting_node, as_ghost=False):
    instruction_index = 0
    current_node = starting_node
    nb_steps = 0

    # The as_ghost parameter is for the part 2. Instead of stopping when the current node is 'ZZZ', we simply stop
    # when the current node ends in Z
    while (as_ghost is False and current_node != 'ZZZ') or (as_ghost is True and not current_node.endswith('Z')):
        if instructions[instruction_index] == 'L':
            current_node = nodes[current_node].left
        elif instructions[instruction_index] == 'R':
            current_node = nodes[current_node].right
        else:
            print(f"Unknown instruction: {instructions[instruction_index]}")

        instruction_index = (instruction_index + 1) % len(instructions)
        nb_steps += 1

    return nb_steps


def lookup_nodes_as_ghost(instructions, nodes):
    # Find our ghosts by looking at node ending in A
    current_nodes = [node for node in nodes.keys() if node.endswith('A')]
    return lcm_of_list([lookup_nodes(instructions, nodes, node, as_ghost=True) for node in current_nodes])


def day8_1(file):
    instructions, nodes = parse_file(file)
    print(lookup_nodes(instructions, nodes, 'AAA'))


def day8_2(file):
    # In this part, we cannot proceed as in part 1, as the number of iterations required is extremely high. Instead,
    # the idea is to look at the minimum number of steps required for each ghost and calculate the LCM of
    # these numbers.
    instructions, nodes = parse_file(file)
    print(lookup_nodes_as_ghost(instructions, nodes))


if __name__ == '__main__':
    day8_1(sys.argv[1])
    day8_2(sys.argv[1])

