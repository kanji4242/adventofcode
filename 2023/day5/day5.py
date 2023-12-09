#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/5
#

import sys
import re


def parse_almanac(file):
    almanac = {"seeds": None, "maps": []}
    current_map_ranges = []

    with open(file) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("seeds: "):
                match = re.search(r"seeds: (.+)", line)
                seeds = list(map(int, match.group(1).split(' ')))
                almanac["seeds"] = seeds

            elif line.endswith(" map:"):
                if current_map_ranges:
                    almanac["maps"].append(current_map_ranges)

                current_map_ranges = []

            elif re.search(r"[\d ]+", line):
                current_map_ranges.append(list(map(int, line.split(' '))))

    if current_map_ranges:
        almanac["maps"].append(current_map_ranges)

    return almanac


def find_lowest_location(almanac):
    locations = []

    for seed in almanac['seeds']:
        for mapping in almanac['maps']:
            print('====')
            for rg in mapping:
                if rg[1] <= seed < rg[1] + rg[2]:
                    new_seed = seed - (rg[1] - rg[0])
                    print(rg, f"{rg[1]}-{rg[1] + rg[2]} => {rg[0]}-{rg[0] + rg[2]}", seed, "->", new_seed)
                    seed = new_seed
                    break

        locations.append(seed)

    return min(locations)


def process_map(src_range, map_ranges):
    dst_range = []
    map_ranges = sorted(map_ranges, key=lambda x: x[0])
    min_range = min([rg[0] for rg in map_ranges])
    max_range = max([rg[1] for rg in map_ranges])
    print("\n---", src_range, map_ranges)

    print("min", min_range, "max", max_range)
    if (src_range[0] < min_range and src_range[0] < min_range) \
            or (src_range[1] > max_range and src_range[1] > max_range):
        dst_range = src_range
        print("outside")
        return [dst_range]

    if src_range[0] < min_range:
        print("partial outside_min")
        dst_range.append((src_range[0], min_range - 1))

    for n in range(len(map_ranges)):
        map_range = map_ranges[n]
        offset = map_ranges[n][2]
        print(f"{map_range[0]} => {map_range[1]}, offset: {map_range[2]}")
        if map_range[0] <= src_range[0] <= map_range[1] and src_range[1] >= map_range[1]:
            print("map_range above")
            dst_range.append((src_range[0] + offset, map_range[1] + offset))
        elif map_range[0] <= src_range[1] <= map_range[1] and src_range[0] <= map_range[0]:
            print("map_range below")
            dst_range.append((map_range[0] + offset, src_range[1] + offset))
        elif src_range[0] >= map_range[0] and src_range[1] <= map_range[1]:
            print("map_range inside")
            dst_range.append((src_range[0] + offset, src_range[1] + offset))
        else:
            print("map outside")

        if n < len(map_ranges) - 2 and map_range[1] + 1 > map_ranges[n + 1][0]:
            dst_range.append((map_range[1] + 1, map_ranges[n + 1][0]))

    if src_range[1] > max_range:
        print("partial outside_max")
        dst_range.append((max_range + 1, src_range[1]))

    print("ret", dst_range)
    return dst_range


def find_lowest_location_with_range(almanac):
    location_ranges = []
    seed_ranges = [(almanac['seeds'][i], almanac['seeds'][i] + almanac['seeds'][i + 1] - 1)
                   for i in range(0, len(almanac['seeds']) - 1, 2)]

    new_ranges = []
    current_ranges = seed_ranges
    for map_range in almanac['maps']:
        print("\n---- new map ----")
        for rg in current_ranges:
            new_ranges.extend(process_map(rg, [(rg[1], rg[1] + rg[2] - 1, - (rg[1] - rg[0])) for rg in map_range]))
        current_ranges = list(set(new_ranges))
        new_ranges = []
        print("Res:", current_ranges)

    return min([x[0] for x in current_ranges])

def find_lowest_location_with_range_old(almanac):
    # for mapping in almanac['maps']:
    #    print("=====")
    #    for rg in sorted(mapping, key=lambda x: x[1]):
    #        print(rg, f"{rg[1]}-{rg[1] + rg[2]} => {rg[0]}-{rg[0] + rg[2]}")

    # return

    location_ranges = []
    seed_ranges = [(almanac['seeds'][i], almanac['seeds'][i] + almanac['seeds'][i + 1] - 1)
                   for i in range(0, len(almanac['seeds']) - 1, 2)]

    for seed_range in seed_ranges:
        seed_location_ranges = [seed_range]
        print("seed", seed_location_ranges)

        for mapping in almanac['maps']:
            print("map")
            mapping_location_ranges_to = []
            for mapping_location_range in seed_location_ranges:
                for rg in mapping:
                    rg_from, rg_to = rg[1], rg[1] + rg[2] - 1
                    offset = - (rg[1] - rg[0])
                    print("rg", rg_from, rg_to, offset)

                    if mapping_location_range[0] < rg_from and mapping_location_range[1] < rg_from:
                        mapping_location_ranges_to.append((mapping_location_range[0], mapping_location_range[1]))

                    elif mapping_location_range[0] < rg_from <= mapping_location_range[1] <= rg_to:
                        mapping_location_ranges_to.extend([
                            (mapping_location_range[0], rg_from - 1),
                            (rg_from + offset, mapping_location_range[1] + offset)
                        ])

                    elif rg_from <= mapping_location_range[0] <= rg_to \
                            and rg_from <= mapping_location_range[1] <= rg_to:
                        mapping_location_ranges_to.extend([
                            (mapping_location_range[0] + offset, mapping_location_range[1] + offset)
                        ])

                    elif rg_from <= mapping_location_range[0] <= rg_to < mapping_location_range[1]:
                        mapping_location_ranges_to.extend([
                            (mapping_location_range[0] + offset, rg_to + offset),
                            (rg_to + 1, mapping_location_range[1])
                        ])

                    elif mapping_location_range[0] > rg_to and mapping_location_range[1] > rg_to:
                        mapping_location_ranges_to.append((mapping_location_range[0], mapping_location_range[1]))

            seed_location_ranges = list(set(mapping_location_ranges_to))

            print(seed_location_ranges)
        seed_location_ranges.extend(seed_location_ranges)

        location_ranges.extend(seed_location_ranges)

    return min([x[0] for x in location_ranges])


def day5_1(file):
    print(find_lowest_location(parse_almanac(file)))


def day5_2(file):
    print(find_lowest_location_with_range(parse_almanac(file)))


if __name__ == '__main__':
    # day5_1(sys.argv[1])
    day5_2(sys.argv[1])
