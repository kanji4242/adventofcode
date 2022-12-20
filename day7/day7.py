#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/7
#

import sys


def display_tree(path, root):
    for entry in root.keys():
        if entry == "..":
            continue
        if type(root[entry]) is dict:
            display_tree(path + "/" + entry, root[entry])
        elif type(root[entry]) is int:
            print(path + "/" + entry, root[entry])


def day7_1(file):
    root = {}
    pwd = root
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("$ "):
                if line.startswith("$ cd"):
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

    print(pwd)
    display_tree("", root)


def day7_2(file):
    with open(file) as f:
        for line in f:
            pass


if __name__ == '__main__':
    day7_1(sys.argv[1])
    #day7_2(sys.argv[1])

