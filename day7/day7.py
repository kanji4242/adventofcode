#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/7
#

import sys


def parse_input(file):
    pwd = root = {}
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("$ cd "):
                if line[5:].strip() == "..":
                    pwd = pwd[".."]
                elif line[5:].strip() in pwd:
                    pwd = pwd[line[5:].strip()]
            else:
                size_or_dir, entry = line.split(" ")
                if size_or_dir.isdigit():
                    pwd[entry] = int(size_or_dir)
                elif size_or_dir == "dir":
                    pwd[entry] = {"..": pwd}
    return root


def display_tree(path, root):
    for entry, value in root.items():
        if entry != ".." and type(value) is dict:
            display_tree(path + "/" + entry, value)
        elif type(value) is int:
            print(path + "/" + entry, value)


def compute_size(root, partial_size=0):
    used_size = 0
    for entry, value in root.items():
        if entry != ".." and type(value) is dict:
            dir_size, partial_size = compute_size(value, partial_size)
            used_size += dir_size
            if dir_size <= 100_000:
                partial_size += dir_size
        elif type(value) is int:
            used_size += value
    return used_size, partial_size


def find_size_to_delete(root, used_size, size_to_delete=70_000_000):
    tmp_size = 0
    for entry, value in root.items():
        if entry != ".." and type(value) is dict:
            dir_size, size_to_delete = find_size_to_delete(value, used_size, size_to_delete)
            tmp_size += dir_size
            if size_to_delete > dir_size > (-40_000_000 + used_size):
                size_to_delete = dir_size
        elif type(value) is int:
            tmp_size += value
    return tmp_size, size_to_delete


def day7_1(file):
    root = parse_input(file)
    print(compute_size(root)[1])


def day7_2(file):
    root = parse_input(file)
    used_size, partial_size = compute_size(root)
    print(find_size_to_delete(root, used_size)[1])


if __name__ == '__main__':
    #day7_1(sys.argv[1])
    day7_2(sys.argv[1])

