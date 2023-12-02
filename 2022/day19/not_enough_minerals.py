#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from typing import List, Any

import sys
import re
from cvxopt.glpk import ilp
from cvxopt import matrix


def read_file_into_list(
        path: str,
        split_list_char: str = None,
        drop_spaces: bool = True
) -> list:
    with open(path) as f:
        lines = f.readlines()
    if split_list_char is not None:
        cuts = [i for i, x in enumerate(lines) if x == split_list_char]
        cuts = [0] + cuts + [len(lines)]
        lines = [[s for s in lines[i:j]] for i, j in zip(cuts[:(len(cuts) - 1)], cuts[1:len(cuts)])]
    return clean_string_list(lines, drop_spaces=drop_spaces)


def clean_string_list(
        l: str,
        drop_spaces: bool = True
) -> list:
    def _clean_string(s: str) -> str:
        s = s.strip() if drop_spaces else s.replace('\n', '')
        return s if len(s) > 0 else None

    l = [(_clean_string(s) if not isinstance(s, list) else clean_string_list(s, drop_spaces=drop_spaces)) for s in l]
    l = [s for s in l if s is not None]
    return l if len(l) > 0 else None


def process_blueprint(line: str) -> tuple:
    print("process_blueprint", line)
    bid = int(re.search('Blueprint (\d+?):', line).group(1))
    ore_ore = int(re.search('Each ore robot costs (\d+?) ore.', line).group(1))
    clay_ore = int(re.search('Each clay robot costs (\d+?) ore.', line).group(1))
    obsidian_ore = int(re.search('Each obsidian robot costs (\d+?) ore', line).group(1))
    obsidian_clay = int(re.search('Each obsidian robot costs \d+ ore and (\d+?) clay.', line).group(1))
    geode_ore = int(re.search('Each geode robot costs (\d+?) ore', line).group(1))
    geode_obsidian = int(re.search('Each geode robot costs \d+ ore and (\d+?) obsidian.', line).group(1))
    cost = {
        'ore': {'ore': ore_ore, 'clay': 0, 'obsidian': 0},
        'clay': {'ore': clay_ore, 'clay': 0, 'obsidian': 0},
        'obsidian': {'ore': obsidian_ore, 'clay': obsidian_clay, 'obsidian': 0},
        'geode': {'ore': geode_ore, 'clay': 0, 'obsidian': geode_obsidian}
    }
    return bid, cost


def process_input(input: list) -> dict:
    return {id: cost for id, cost in [process_blueprint(l) for l in input]}


def count_max_geodas(
        blueprint: dict,
        max_time: int,
        starting_robots: dict = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0},
        starting_minerals: dict = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
) -> int:
    max_geodes = 0
    options = [(1, starting_robots, starting_minerals)]
    while len(options) > 0:
        time, robots, minerals = options.pop(0)
        max_geodes = max(max_geodes, minerals['geode'] + robots['geode'])
        if time == max_time:
            continue
        for robot_to_build in robots:
            cost = blueprint[robot_to_build]
            new_minerals = minerals.copy()
            new_minerals = {m: new_minerals[m] - cost.get(m, 0) for m in new_minerals}
            if min(new_minerals.values()) >= 0:
                new_robots = {r: (n if r != robot_to_build else n + 1) for r, n in robots.items()}
                new_minerals = {m: new_minerals[m] + robots[m] for m in new_minerals}
                options.append((time + 1, new_robots, new_minerals))
        options.append((time + 1, robots, {m: minerals[m] + robots[m] for m in minerals}))
    return max_geodes


def print_obj(obj, max_time):
    print("---or: ", ' '.join([f"{obj[i]:2}" for i in range(0, max_time)]))
    print("---cl: ", ' '.join([f"{obj[i + max_time]:2}" for i in range(0, max_time)]))
    print("---ob: ", ' '.join([f"{obj[i + max_time * 2]:2}" for i in range(0, max_time)]))
    print("---ge: ", ' '.join([f"{obj[i + max_time * 3]:2}" for i in range(0, max_time)]))
    print("")

def linear_optimization(
        blueprint: dict,
        max_time: int
) -> List[Any]:
    # Variables:
    # - Number of ore / clay / obsidian / geode robots at start of minute i
    obj = [0] * max_time + [0] * max_time + [0] * max_time + \
          [-(max_time - i) for i in range(max_time)]
    nvars = len(obj)
    lhs_ineq = []
    rhs_ineq = []
    # Current number of robots never higher than the total materials needed minus used
    for m1_idx, m1 in enumerate(blueprint):
        print("==== robot ", m1_idx, m1)
        for m2_idx, (m2, v) in enumerate(blueprint[m1].items()):
            print("====== it costs", m2_idx, (m2, v))
            if v > 0:
                for i in range(1, max_time):
                    lhs_ineq_i = [0] * nvars
                    lhs_ineq_i[m1_idx * max_time + i] = blueprint[m1][m2]
                    for j in range(i - 1):
                        lhs_ineq_i[m2_idx * max_time + j] = -1
                    for k, cost in enumerate(blueprint.values()):
                        if k != m1_idx:
                            lhs_ineq_i[k * max_time + i - 1] += cost[m2]
                    #print_obj(lhs_ineq_i, max_time)
                    #print(0 if m2 != 'ore' else blueprint[m2][m2])
                    lhs_ineq.append(lhs_ineq_i)
                    rhs_ineq.append(0 if m2 != 'ore' else blueprint[m2][m2])
                    print_obj(lhs_ineq_i, max_time)
                    print("---")
                    #print(0 if m2 != 'ore' else blueprint[m2][m2])
    # Current number of robots at most 1 more than in previous step
    for i in range(1, max_time):
        lhs_ineq_i = [0] * nvars
        for j in range(len(blueprint)):
            lhs_ineq_i[j * max_time + i] = 1
            lhs_ineq_i[j * max_time + i - 1] = -1
        lhs_ineq.append(lhs_ineq_i)
        rhs_ineq.append(1)
        #print_obj(lhs_ineq_i, max_time)
    # Not possible to lose robots
    for i in range(len(blueprint)):
        for j in range(1, max_time):
            lhs_ineq_j = [0] * nvars
            lhs_ineq_j[i * max_time + j] = -1
            lhs_ineq_j[i * max_time + j - 1] = 1
            #print_obj(lhs_ineq_j, max_time)
            lhs_ineq.append(lhs_ineq_j)
            rhs_ineq.append(0)
    # Starting with just one ore robot
    lhs_eq = []
    rhs_eq = []
    for i in range(len(blueprint)):
        lhs_eq_i = [0] * nvars
        lhs_eq_i[i * max_time] = 1
        lhs_eq.append(lhs_eq_i)
        rhs_eq.append((1 if i == 0 else 0))

    with open("/tmp/day19.out2", "w") as f:
        f.write("c\n")
        f.write(str(matrix(obj, tc='d')))
        f.write("G\n")
        f.write(str(matrix(lhs_ineq, tc='d').T))
        f.write("h\n")
        f.write(str(matrix(rhs_ineq, tc='d')))
        f.write("A\n")
        f.write(str(matrix(lhs_eq, tc='d').T))
        f.write("b\n")
        f.write(str(matrix(rhs_eq, tc='d')))
        f.write("I\n")
        f.write(str(set(range(len(obj)))))

    # Optimum
    #print_obj(obj, max_time)
    print(rhs_ineq)
    (_, x) = ilp(c=matrix(obj, tc='d'),
                 G=matrix(lhs_ineq, tc='d').T,
                 h=matrix(rhs_ineq, tc='d'),
                 A=matrix(lhs_eq, tc='d').T,
                 b=matrix(rhs_eq, tc='d'),
                 I=set(range(len(obj))))
    print(x)
    return list(x[(3 * max_time):(4 * max_time)])


def count_geodes(
        blueprint: dict,
        max_time: int
) -> int:
    geode_times = linear_optimization(blueprint, max_time)
    print(geode_times, len(geode_times), range(int(max(geode_times))))
    counts = [len(geode_times) - geode_times.index(i + 1) for i in range(int(max(geode_times)))]
    print(counts)
    print(f"Geodes: ", sum(counts))
    return sum(counts)


def determine_quality_level(
        blueprints: dict,
        max_time: int
) -> int:
    quality = 0
    for bid, blueprint in blueprints.items():
        n = count_geodes(blueprint, max_time)
        quality += bid * n
    return quality


def determine_top_values(
        blueprints: dict,
        max_time: int,
        top: int = 3
) -> int:
    value = 1
    for i in range(min(top, len(blueprints))):
        blueprint = blueprints[i + 1]
        n = count_geodes(blueprint, max_time)
        value *= n
    return value


def day19_1(file):
    input = read_file_into_list(path=file)
    blueprints = process_input(input)
    answer = determine_quality_level(blueprints, max_time=24)
    print(f'Answer to part 1: {answer}')

    #answer = determine_top_values(blueprints, max_time=32, top=3)
    #print(f'Answer to part 2: {answer}')


if __name__ == '__main__':
    day19_1(sys.argv[1])
