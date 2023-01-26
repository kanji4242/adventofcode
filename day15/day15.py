#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/15
#

import sys
import re


def read_sensors(file):
    sensors = []
    with open(file) as f:
        for line in f:
            if m := re.match(r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)',
                             line.strip()):
                sensors.append(tuple([int(x) for x in list(m.groups())]))

    return sensors


def get_manhattan_distance(s):
    return abs(s[1] - s[3]) + abs(s[0] - s[2])


def add_sensor_edges(sensor):
    points = []
    manhattan_distance = get_manhattan_distance(sensor) + 1

    points.append((sensor[0] - manhattan_distance, sensor[1]))
    points.append((sensor[0] + manhattan_distance, sensor[1]))
    for md in range(- manhattan_distance + 1, manhattan_distance):
        points.append((sensor[0] + md, sensor[1] + abs(md) - manhattan_distance))
        points.append((sensor[0] + md, sensor[1] - abs(md) + manhattan_distance))

    return points


def is_covered(point, sensors):
    covered = False
    for s in sensors:
        manhattan_distance = get_manhattan_distance(s)
        if (abs(point[0] - s[0]) + abs(point[1] - s[1])) <= manhattan_distance:
            covered = True
            break
    return covered


def get_sensors_boundary(sensors, with_md=False):
    if with_md:
        return (min([s[0] - get_manhattan_distance(s) for s in sensors]),
                max([s[0] + get_manhattan_distance(s) for s in sensors]),
                min([s[1] - get_manhattan_distance(s) for s in sensors]),
                max([s[1] + get_manhattan_distance(s) for s in sensors]))
    else:
        return (min([s[0] for s in sensors]),
                max([s[0] for s in sensors]),
                min([s[1] for s in sensors]),
                max([s[1] for s in sensors]))


def clean_edges(points, sensors):
    return list(filter(lambda p: not is_covered(p, sensors), points))


def crop_area(points, boundary):
    return list(filter(
        lambda p: (boundary[0] <= p[0] <= boundary[1]) and (boundary[2] <= p[1] <= boundary[3]),
        points))


def day15_1(file, line_no=10):
    sensors = read_sensors(file)
    boundary = get_sensors_boundary(sensors, with_md=True)
    print("Sensors boundary with manhattan distance:", boundary)

    beacons = list(set([(s[2], s[3]) for s in sensors]))
    print("Unique beacon:", len(beacons))
    beacons_line_no = len(list(filter(lambda b: b[1] == line_no, beacons)))
    print(f"Unique beacon at line {line_no}:", beacons_line_no)

    cell_covered = len(list(filter(lambda x: is_covered((x, line_no), sensors),
                                   list(range(boundary[0], boundary[1] + 1)))))
    print(cell_covered - beacons_line_no)


def day15_2(file):
    sensors = read_sensors(file)
    boundary = get_sensors_boundary(sensors)
    print("Sensors boundary:", boundary)

    points = []
    for i in range(len(sensors)):
        s = sensors[i]
        print("Processing sensor:", s, "manhattan distance: ", get_manhattan_distance(s),
              f"(+{(get_manhattan_distance(s) + 1) * 4})")
        points.extend(add_sensor_edges(s))
        print("Points nb:", len(points))
        print("")

    pe = len(points)
    points = clean_edges(points, sensors[:i + 1])
    print("Cleaned Points nb:", len(points), f"({len(points) - pe})")
    points = crop_area(points, boundary)
    print("Cropped Points nb:", len(points), len(set(points)))

    tuning_freq = list(set(points))[0][0] * 4_000_000 + list(set(points))[0][1]
    print(tuning_freq)


if __name__ == '__main__':
    day15_1(sys.argv[1], line_no=2_000_000)
    day15_2(sys.argv[1])

