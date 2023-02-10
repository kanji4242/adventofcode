#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/15
#

import sys
import re


def read_sensors(file):
    # REad all sensors information and insert into in a list
    sensors = []
    with open(file) as f:
        for line in f:
            if m := re.match(r'Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)',
                             line.strip()):
                sensors.append(tuple([int(x) for x in list(m.groups())]))

    return sensors


def get_manhattan_distance(s):
    # Find the Manhattan distance between the sensor and its beacon
    # This is simply the sum of the absolute values of the differences in both coordinates.
    return abs(s[1] - s[3]) + abs(s[0] - s[2])


def add_sensor_edges(sensor):
    # Returns all point coordinate that below to the edge of a sensor area with its beacon.
    # The edge of a sensor area are all point that are a direct neighbor of the area boundary
    # For instance, a sensor located at [4, 4] and its beacon located at [2, 6], the method will return
    # the following points coordinates marked as "E" ("S" is the sensor, "B" is the beacon):
    #      0    5
    #    ......E.....
    #  0 .....E.E....
    #    ....E...E...
    #    ...E.....E..
    #    ..E.......E.
    #    .E....S....E
    #  5 ..E.......E.
    #    ...EB....E..
    #    ....E...E...
    #    .....E.E....
    #    ......E.....
    points = []
    manhattan_distance = get_manhattan_distance(sensor) + 1

    points.append((sensor[0] - manhattan_distance, sensor[1]))
    points.append((sensor[0] + manhattan_distance, sensor[1]))
    for md in range(- manhattan_distance + 1, manhattan_distance):
        points.append((sensor[0] + md, sensor[1] + abs(md) - manhattan_distance))
        points.append((sensor[0] + md, sensor[1] - abs(md) + manhattan_distance))

    return points


def is_covered(point, sensors):
    # Determine if a point is within the area covered of at least one sensor given in the list
    # The area of sensor depend on its beacon and their Manhattan distance and has a rhombus shape.
    # For instance, a sensor located at [4, 4] and its beacon located at [2, 6] have a Manhattan distance of 4
    # Their area will look like a rhombus centered at [4, 4] with all its 4 edges locate 4 units away.
    # Every point marked "#" has a Manhattan distance less or equal to 4 with the sensor.
    # Given this area, a point X at [0, 2] will be outside the area, while a point Y at [5, 6] will be inside.
    # ("S" is the sensor, "B" is the beacon, "X" and "Y" are the 2 points mentioned above)
    #     0   4   8
    #  0 .....#....
    #    ....###...
    #    .X.#####..
    #    ..#######.
    #  4 .####S####
    #    ..#######.
    #    ...B##Y#..
    #    ....###...
    #  8 .....#....
    #
    # This check is performed for every sensor provided in the list. If the point is found inside a sensor area
    # the method returns True
    covered = False
    for s in sensors:
        manhattan_distance = get_manhattan_distance(s)
        if (abs(point[0] - s[0]) + abs(point[1] - s[1])) <= manhattan_distance:
            covered = True
            break
    return covered


def get_sensors_boundary(sensors, with_md=False):
    # Determine the minimum and the maximum coordinates for a list sensors
    # if with_md is defined, consider the area covered with its beacon and using its Manhattan distance
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
    # Find the boundaries of all sensors including their area. With this information we have a range
    # of coordinates to work with
    boundary = get_sensors_boundary(sensors, with_md=True)
    print("Sensors boundary with manhattan distance:", boundary)

    # Get the beacon coordinates to delete them because beacons do not count on the result
    beacons = list(set([(s[2], s[3]) for s in sensors]))
    print("Unique beacon:", len(beacons))
    # Find the number of beacon located on the considered line
    beacons_line_no = len(list(filter(lambda b: b[1] == line_no, beacons)))
    print(f"Unique beacon at line {line_no}:", beacons_line_no)

    # Get the number of points covered by all sensors
    cell_covered = len(list(filter(lambda x: is_covered((x, line_no), sensors),
                                   list(range(boundary[0], boundary[1] + 1)))))

    # Returns this number without the number of beacon found previously
    print(cell_covered - beacons_line_no)


def day15_2(file):
    sensors = read_sensors(file)
    boundary = get_sensors_boundary(sensors)
    print("Sensors boundary:", boundary)

    # The part2 is trickier, we need to find a single point not covered by any sensor.
    # The problem is that the grid is far too big, we cannot work with a numpy array because it would require
    # several EiB of RAM memory to store it. So we need to find another way.
    # We can notice that this point is a single point, so it must lie on an edge of several sensors.
    # So the idea is to focus on the edges point of an area instead of the area points themselves, this approach
    # will drastically reduce the memory needed.
    # We place in a list the edge points of the first sensor, append to the list the edge points of the second
    # sensor, do the same for third one, and so on and so forth.
    # Then delete the edge points we have in the list covered by any of all sensors.
    # We also filter (crop) the points, because by definition the point cannot lie belong any sensor location.
    # And at the end, we should have few points with the same coordinate because this single point belong to edge
    # of several sensors. And this point is the answer.
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

