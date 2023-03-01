#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/19
#

"""
For this problem we will implement a numerical solution instead of the more obvious option of using a graph
representation of the possibilities. In order to do that, we will model the problem as a set of inequalities
and equalities and use the integer linear programming (ILP) implementation from the cvxopt library to find a
maximum value. One of the advantages of this approach is that the computation is almost instantaneous.

To solve this problem, we will use a set of variables that will represent the count of robots from type 'x' available
at the beginning of minute 'i'. We will denote them as Rx_i will be. For instance, the count of robots from type
'clay' at minute '12" will be noted Rclay_12. With this configuration, we have a total of 24∗4 = 96 variables
for the part 1 and 32 ∗ 4 = 128 for the part 2 :

For instance, for the part 1 will have the following set of variables :
{ Rore_1, ... , Rore_24, Rclay_1, ... , Rclay_24, Robs_1, ... , Robs_24, Rgeo_1, ... , Rgeo_24 }   

If we denote as T the total count of minutes (24 and 32 for each
part respectively), the formula that we want to maximize is the geodes produced eight minute weighted by the
current minutes left :

  geode_level = Rgeo_1 * T + Rgeo_2 * (T−1) + ... + Rgeo_T * 1
  
The variables to count robots from other types have weight 0 in this formula, because we're only interested in
geodes.

To perform a ILP we need to provide :
  - a minimizing matrix : related a linear expression involving our variables weighted coefficients which are
    represented by a matrix (a 24x1 matrix for part 1 and 32 x 1 for part 2). The algorithm will try to minimize.
    This expression will be our geode_level, but we want to maximize it. To do that, the trick is use negative numbers.
    So we will use the following matrix : { -T, -T+1, ... , -1 }

  - a set of inequalities expression (LHS) : a set linear expression discussed below related to the expression
    a_n*x + b_n*y + ... <= k_n with all variables moved on the left-hand side (LHS) and the value and right-hand side.
    It will be represented by a matrix like { a_n, b_n, ... }
  - the inequalities values (RHS) : All k_n values represented by a matrix like { k_0, k_1, ... , k_n }

  - a set of equalities expression (LHS) : a set linear expression discussed below related to the expression
    a_n*x + b_n*y + ... = k_n with all variables moved on the left-hand side (LHS) and the value and right-hand side.
    It will be represented by a matrix like { a_n, b_n, ... }
  - the equalities values (RHS) : All k_n values represented by a matrix like { k_0, k_1, ... , k_n }

  - a matrix with the set of indices of our variables

We will complete our setup with the following set of constrains:

1/ The amount of robots of each type on each minute is limited by the materials available to build them until that
minute. That is, the total amount of materials collected until that point minus the materials used to build other
types of robots, divided by the cost. We have to take into account that we start with one ore robot, so we do not
need to subtract its cost. For example, for geode robots costs 2 ores and 7 obsidians, so we have the following two
inequalities for the first example blueprint. The first one is for ore and the second one is for obsidian:

  Rgeo_i <= 1/2 (sum from j=1 to i-2 of all Rore_j) - (4(Rore_i-1 - 1) + 2*Rclay_i-1 + 3*Robs_i-1)
     ==> 2*Rgeo_i - Rore_1 - Rore_2 - ... - Rore_i-2 + 4*Rore_i-1 + 2*Rclay_i-1 + 3*Robs_i-1 <= 4
     
  Rgeo_i <= 1/7 (sum from j=1 to i-2 of all Robs_j)
     ==> 7*Rgeo_i - Robs_1 - Robs_2 - ... - Robs_i-2 <= 0

2/ We can build just one robot at each step. That is, the total count of robots is, at most, one more than the
previous count:

  Rore_i + Rclay_i + Robs_i + Rgeo_i <= Rore_i-1 + Rclay_i-1 + Robs_i-1 + Rgeo_i-1 + 1
     ==> Rore_i + Rclay_i + Robs_i + Rgeo_i - Rore_i-1 - Rclay_i-1 - Robs_i-1 - Rgeo_i-1 <= 1
     
3/ It is not possible to lose robots. That is, the count of robots of each type is, at least, the same as in the
previous step. For example, for ore robots:

  Rore_i−1 <= Rore_i
     ==> Rore_i−1 - Rore_i <= 0

4/ We also define the starting conditions (we just have 1 ore robot) using this equalities:

  Rore_1 = 1, Rclay_1 = 0, Robs_1 = 0, Rgeo_1 = 0 and 0 for all others variables
  
"""

import sys
import re
from cvxopt.glpk import ilp
from cvxopt import matrix

from typing import List


class ResourceSet(list):
    """
    ResourceSet is a set of the 4 resources indexed as follows : ore(0), clay(1), obsidian(2) and geode(3).
    Quantities are initialized to 0. You can access or set quantity by its index number or its name.
    For instance, to set 3 for clay to a ResourceSet named "rs", you can do:
      rs.clay = 3 or rs[1] = 3
    """
    RESOURCES = ["ore", "clay", "obsidian", "geode"]

    def __init__(self):
        super().__init__([0, 0, 0, 0])

    def __str__(self):
        return f"{{{'/'.join([str(self[x]) for x in range(4)])}}}"

    @property
    def size(self):
        return 4

    def __getattr__(self, item):
        try:
            return self[self.RESOURCES.index(item)]
        except ValueError:
            raise AttributeError(f"No such attribute: {item}") from None

    def __setattr__(self, item, value):
        try:
            self[self.RESOURCES.index(item)] = int(value)
        except ValueError:
            raise AttributeError(f"No such attribute: {item}") from None


class RobotMatrix(list):
    """
    RobotMatrix is a list of ResourceSet instances. The size of the list is linked to the number of minutes given
    by the puzzle (24 or 32).
    This a convenient way to assign coefficient to our set of variables described above. The final list can be
    obtained with the as_list() method which will be used to build the matrix for ILP
    For instance, to set 12 for obsidian at minute 10 to a RobotMatrix named "rm", you can do:
      rm[9][2] = 12 or rm[9].obsidian = 12
    With this quantity being set, calling the method as_list() will yield the following list of size "4 * size" with:
      [ "size" * 0s (ore),
        "size" * 0s (clay),
        9 * 0s (obsidian), 12 (our previous set), "size - 10" * 0s (obsidian),
        "size" * 0s (geode) ]
    """
    def __init__(self, size):
        # Set a list with "size" ResourceSet instances
        super().__init__([ResourceSet() for _ in range(size)])

    def __str__(self):
        output = "---or: " + ' '.join([f"{self[i].ore:2}" for i in range(len(self))])
        output += "\n---cl: " + ' '.join([f"{self[i].clay:2}" for i in range(len(self))])
        output += "\n---ob: " + ' '.join([f"{self[i].obsidian:2}" for i in range(len(self))])
        output += "\n---ge: " + ' '.join([f"{self[i].geode:2}" for i in range(len(self))])
        return output

    def as_list(self):
        # Returns the matrix which can be injected in the ILP process
        size = self[0].size
        return [int(self[x][y]) for y in range(size) for x in range(len(self))]


class Robot:
    """
    Robot contains information about its characteristics and contains:
     - its type
     - its cost in terms of resources (a ResourceSet instance).
    """
    def __init__(self, type_label: str, cost: ResourceSet):
        if type_label in ResourceSet.RESOURCES:
            self.type = type_label
            self.type_id = ResourceSet.RESOURCES.index(type_label)
        else:
            raise TypeError(f"Unknown robot type {type_label}")

        self.cost = cost

    def __repr__(self):
        return f"Robot[{self.type}](costs:{self.cost})"


class Blueprint:
    """
    Blueprint contains informations about a blueprint and contains:
     - its ID
     - all the 4 robots characteristics
    """
    def __init__(self, bp_id: int, robots: List[Robot]):
        self.id = bp_id
        self.robots = robots

    def __repr__(self):
        return f"Blueprint#{self.id}(robots:{self.robots})"


def parse_blueprints(file):
    """
    Build and return a list of Blueprint instances set with their ID and their robots characteristics
    """
    blueprints = []
    with open(file) as f:
        content = f.read().replace("\n", " ")
        for bp_line in content.split("Blueprint "):
            robots = list([None] * 4)
            if bp_line:
                bp_id = int(bp_line[:bp_line.find(":")])
                if m1 := re.findall(r'Each (.*?) robot costs (.*?)\.', bp_line):
                    for robot_entry in m1:
                        costs = ResourceSet()
                        for resource in robot_entry[1].split(" and "):
                            if m2 := re.search(r'^(\d+) (.+)$', resource):
                                setattr(costs, m2.group(2), m2.group(1))
                        robot = Robot(robot_entry[0], costs)
                        robots[robot.type_id] = robot
                blueprints.append(Blueprint(bp_id, robots))

    return blueprints


def process_blueprint(blueprint, max_minutes=24):
    lhs_ineq = []
    rhs_ineq = []
    lhs_eq = []
    rhs_eq = []

    # Minimize this expression
    # We do not care about ore, clay, obsidian robots, only geode robots set with coefficients
    # Since we want to maximize the geode robots, we use negative coefficients
    # This is will generate the matrix for geode with { -T, -T+1, ... , -1 } as described abode.
    # All other resources matrices will be set to 0
    minimize = RobotMatrix(max_minutes)
    for i in range(max_minutes):
        minimize[i].geode = -(max_minutes - i)

    # Current number of robots never higher than the total materials needed minus used
    # Based on the example formula described above:
    #   2*Rgeo_i - Rore_1 - Rore_2 - ... - Rore_i-2 + 4*Rore_i-1 + 2*Rclay_i-1 + 3*Robs_i-1 <= 4
    for robot in blueprint.robots:
        for cost_id in range(len(robot.cost)):
            if robot.cost[cost_id] > 0:
                print(robot, robot.cost[cost_id])
                for i in range(1, max_minutes):
                    rm = RobotMatrix(max_minutes)
                    # Set: 2*Rgeo_i
                    rm[i][robot.type_id] = robot.cost[cost_id]

                    # Set: 4*Rore_i-1 + 2*Rclay_i-1 + 3*Robs_i-1
                    for type_id, cost in [(r.type_id, r.cost[cost_id]) for r in blueprint.robots
                                          if r.type_id != robot.type_id]:
                        rm[i - 1][type_id] = cost

                    # Set: - Rore_1 - Rore_2 - ... - Rore_i-2
                    for j in range(i - 1):
                        rm[j][cost_id] = -1

                    # Append to the inequalities matrices list (using as_list())
                    lhs_ineq.append(rm.as_list())

                    # Set: <= 4
                    ore_id = ResourceSet.RESOURCES.index("ore")
                    rhs_ineq.append(0 if cost_id != ore_id else int(blueprint.robots[ore_id].cost.ore))

    # Current number of robots at most 1 more than in previous step
    # Based on the formula described above:
    #   Rore_i + Rclay_i + Robs_i + Rgeo_i - Rore_i-1 - Rclay_i-1 - Robs_i-1 - Rgeo_i-1 <= 1
    for i in range(1, max_minutes):
        rm = RobotMatrix(max_minutes)
        for robot in blueprint.robots:
            # Set: Rore_i - Rore_i-1
            rm[i][robot.type_id] = 1
            rm[i - 1][robot.type_id] = -1

        # Append to the inequalities matrices list (using as_list())
        lhs_ineq.append(rm.as_list())

        # Set: <= 1
        rhs_ineq.append(1)

    # Not possible to lose robots
    # Based on the formula described above:
    #   Rore_i−1 - Rore_i <= 0
    for robot in blueprint.robots:
        for i in range(1, max_minutes):
            rm = RobotMatrix(max_minutes)
            # Set: Rore_i−1 - Rore_i
            rm[i][robot.type_id] = -1
            rm[i - 1][robot.type_id] = 1

            # Append to the inequalities matrices list (using as_list())
            lhs_ineq.append(rm.as_list())

            # Set: <= 0
            rhs_ineq.append(0)

    # Starting with just one ore robot
    #   Rore_1 = 1, Rclay_1 = 0, Robs_1 = 0, Rgeo_1 = 0 and 0 for all others variables
    for robot in blueprint.robots:
        rm = RobotMatrix(max_minutes)
        # Set: 1*Rore_1
        rm[0][robot.type_id] = 1

        # Append to the equalities matrices list (using as_list())
        lhs_eq.append(rm.as_list())

        # Set: = 1 (or ore)
        ore_id = ResourceSet.RESOURCES.index("ore")
        rhs_eq.append((1 if robot.type_id == ore_id else 0))

    # Find optimum
    (_, x) = ilp(c=matrix(minimize.as_list(), tc='d'),
                 G=matrix(lhs_ineq, tc='d').T,
                 h=matrix(rhs_ineq, tc='d'),
                 A=matrix(lhs_eq, tc='d').T,
                 b=matrix(rhs_eq, tc='d'),
                 I=set(range(max_minutes * 4)))

    # x a matrix of size max_minutes x 1. The geode part we're interested in (the Rgeo_x variables) are in the last
    # part of the matrix. Since with have 4 type of resources, and geode is the last one, so they will be in the
    # last quarter of the matrix.
    return int(sum(x[(3 * max_minutes):(4 * max_minutes)]))


def day19_1(file):
    blueprints = parse_blueprints(file)
    quality_level = 0

    for blueprint in blueprints:
        # Iterate over all the blueprints found and set the quality level based on the maximum geode and the
        # blueprint ID
        quality_level += process_blueprint(blueprint, max_minutes=24) * blueprint.id

    print(quality_level)


def day19_2(file):
    blueprints = parse_blueprints(file)
    quality_level = 1

    for blueprint in blueprints[:3]:
        # Iterate over the 3 first blueprints and multiply their maximum geode
        quality_level *= process_blueprint(blueprint, max_minutes=32)

    print(quality_level)


if __name__ == '__main__':
    day19_1(sys.argv[1])
    day19_2(sys.argv[1])
