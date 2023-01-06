#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/12
#

import sys
import numpy as np
from queue import Queue


def level(ch):
    if ch == 'S':
        ch = "a"
    elif ch == 'E':
        ch = "z"
    return ord(ch) - ord('a')


def find_shortest_path(heightmap, start, end):
    queue = Queue()
    queue.put(start)

    path = {start: 0}
    pathmap = np.chararray(heightmap.shape, itemsize=3)
    pathmap[:] = "."

    pathmap[start[0]][start[1]] = 0

    while not queue.empty():
        current = queue.get()
        #print("get", current, end)

        if current == end:
            return max(list(path.values()))

        for neighbor in [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1)
        ]:
            if 0 <= neighbor[0] < heightmap.shape[0] and 0 <= neighbor[1] < heightmap.shape[1]:
                #print("inspect", path[current], neighbor, heightmap[neighbor[0]][neighbor[1]], heightmap[current[0]][current[1]])
                #print_array_bytes(pathmap)
                if (neighbor not in path or path[neighbor] > path[current] + 1) \
                        and heightmap[current[0]][current[1]] <= heightmap[neighbor[0]][neighbor[1]] <= heightmap[current[0]][current[1]] + 1:
                    queue.put(neighbor)
                    #print("put", neighbor)
                    path[neighbor] = path[current] + 1
                    pathmap[neighbor[0]][neighbor[1]] = str(path[current] + 1)

    print_array_all(heightmap, pathmap)
    return "No path found"


def print_array_int(array):
    for x in range(array.shape[0]):
        print(" ".join([f"{y:02}" for y in array[x]]))


def print_array_bytes(array):
    for x in range(array.shape[0]):
        print(" ".join([f"{y.decode('utf-8'):2}" for y in array[x]]))

def print_array_all(array_map, array_path):
    print(array_map.shape, array_path.shape)
    for x in range(array_map.shape[0]):
        print(" ".join([f"{y[0]:02}-{y[1].decode('utf-8'):3}" for y in zip(array_map[x][41:74], array_path[x][41:74])]))



def day12_1(file):
    grid = None
    start_coord = None
    end_coord = None

    with open(file) as f:
        n = 0
        for line in f:
            line = line.rstrip()
            if grid is None:
                grid = np.array(list([level(x) for x in line]), dtype=int)
            else:
                grid = np.vstack((grid, np.array(list([level(x) for x in line]))))
            if line.find("S") >= 0:
                start_coord = (n, line.find("S"))
            if line.find("E") >= 0:
                end_coord = (n, line.find("E"))
            n += 1

    print(start_coord, end_coord)
    print_array_int(grid)
    print(find_shortest_path(grid, start_coord, end_coord))



def day12_2(file):
    with open(file) as f:
        for line in f:
            pass


if __name__ == '__main__':
    day12_1(sys.argv[1])
    #day12_2(sys.argv[1])

