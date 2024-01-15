#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/15
#

import sys
import re


class Lens:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

    def __repr__(self):
        return f"Lens({self.label} {self.focal_length})"


# Define a Box class to represent a box for lenses.
class Box:
    def __init__(self, box_id):
        # Initialize a Box object with a unique identifier (id) and an empty list to store lenses.
        self.id = box_id
        self.lenses = []

    def __repr__(self):
        return f"Box[{self.id}]({' '.join([repr(l) for l in self.lenses])})"

    def add_lens(self, lens):
        # Add a lens to the Box. If a lens with the same label already exists, replace it; otherwise, add the new lens.
        lens_index = self.find_lens(lens.label)
        if lens_index >= 0:
            self.lenses[lens_index] = lens
        else:
            self.lenses.append(lens)

    def find_lens(self, lens_label):
        # Find the index of a lens with a specific label within the list of lenses.
        for n in range(len(self.lenses)):
            if self.lenses[n].label == lens_label:
                return n
        return -1

    def remove_lens(self, lens_label):
        # Remove a lens with a specific label from the list of lenses.
        lens_index = self.find_lens(lens_label)
        if lens_index >= 0:
            self.lenses.pop(lens_index)

    @property
    def focusing_power(self):
        # Compute the focusing power of the Box based on its lenses and their focal lengths.
        value = 0
        for n in range(len(self.lenses)):
            value += (self.id + 1) * (n + 1) * self.lenses[n].focal_length
        return value


def str2hash(string):
    current_hash = 0
    for ch in string:
        current_hash = ((current_hash + ord(ch)) * 17) % 256

    return current_hash


def parse_file(file):
    with open(file) as f:
        steps = f.readline().rstrip().split(',')

    return steps


def find_sum(steps):
    result = 0

    for step in steps:
        result += str2hash(step)

    return result


def operate_lenses(steps):
    # Create an empty list to store Box objects.
    boxes = []

    # Initialize 256 Box objects with different indices and append them to the 'boxes' list.
    for n in range(256):
        boxes.append(Box(n))

    # Iterate through each step in the 'steps' list.
    for step in steps:
        # Use regular expression to match the step format
        match = re.search(r"(\w+)([=-])(\d*)", step)

        if match:
            # Extract information label, operation and eventually the focal length
            lens_label = match.group(1)
            operation = match.group(2)
            focal_length = int(match.group(3)) if match.group(3) else None

            # Add a new lens or replace an existing lens
            if operation == "=":
                # Add or replace the Lens with the given label and focal length to the corresponding Box.
                if focal_length:
                    box_id = str2hash(lens_label)
                    boxes[box_id].add_lens(Lens(lens_label, focal_length))

            # Remove a lens
            elif operation == "-":
                # Remove the lens with the given label from all Boxes.
                for n in range(256):
                    boxes[n].remove_lens(lens_label)

            else:
                print(f"Invalid operation {operation}")

    # Compute the focusing power of all Boxes.
    return sum([b.focusing_power for b in boxes])


def day15_1(file):
    print(find_sum(parse_file(file)))


def day15_2(file):
    print(operate_lenses(parse_file(file)))


if __name__ == '__main__':
    day15_1(sys.argv[1])
    day15_2(sys.argv[1])

