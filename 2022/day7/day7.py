#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/7
#

import sys


def parse_input(file):
    # Parse input lines and build the filesystem tree with a data structure composed of nested dicts
    # Each dict represents a directory where each key represents an entry found (file/dir) in this directory.
    # The name of these keys is the name of this entry
    # The value associated with these keys can be of 2 types :
    #  - an int, which corresponds to a file and the value is its size
    #  - a dict, which corresponds to a subdirectory
    # The dict has also a special key ".." which point to the parent directory, except of the root directory

    # We start with a root (an empty dict)
    # pwd will be a pointer to the current directory/dict and will travel from directory to subdirectory or parent
    # directory during the parsing
    pwd = root = {}
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("$ cd "):
                # If we have a "cd <something>" command, we're entering to another directory, we update the pwd
                # pointer value to this new directory
                if line[5:].strip() == "..":
                    pwd = pwd[".."]
                elif line[5:].strip() in pwd:
                    pwd = pwd[line[5:].strip()]
            else:
                # Otherwise, we consider this line is the directory list
                # Its syntax has 2 syntax : "dir <dirname>" or "<size> <filename>"
                size_or_dir, entry = line.split(" ")
                # We consider that if the 1st word is a number, it's a file
                if size_or_dir.isdigit():
                    # New entry for a file with its size
                    pwd[entry] = int(size_or_dir)
                elif size_or_dir == "dir":
                    # If the 1st word is "dir", it's a subdirectory
                    # New entry for this subdirectory and its parent (".." entry) is set to the current directory
                    pwd[entry] = {"..": pwd}
    return root


def display_tree(path, root):
    # For debugging purpose only
    # Display the directory tree
    for entry, value in root.items():
        if entry != ".." and type(value) is dict:
            display_tree(path + "/" + entry, value)
        elif type(value) is int:
            print(path + "/" + entry, value)


def compute_size(root, partial_size=0):
    # Compute the total size recursively
    # Since we need to find all the directories with a total size of at most 100000, the function returns 2 values :
    #  - used_size: which the real total size ignoring the 100000 limitation, this will be useful for part 2
    #  - partial_size : which total size only for directories whose size are at most 100000
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
    # Find the smallest directory to free up enough space on the filesystem
    # We need the real total given by the function compute_size (used_size parameter), the function returns 2 values :
    # - tmp_size: which the total size of the subdirectory
    # - size_to_delete : is the size to delete, we assume at beginning the best choice is completely free the
    #   filesystem, explaining why it is initialed with the filesystem size, this parameter is updated only if a
    #   better size is found
    tmp_size = 0
    for entry, value in root.items():
        if entry != ".." and type(value) is dict:
            dir_size, size_to_delete = find_size_to_delete(value, used_size, size_to_delete)
            tmp_size += dir_size
            # Compare size to delete we already to the size of the directory previously found, and update
            # size_to_delete if this is better
            # -40_000_000 is just 30_000_000 - 70_000_000
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
    day7_1(sys.argv[1])
    day7_2(sys.argv[1])

