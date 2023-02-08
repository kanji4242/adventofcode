#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/16
#

import sys
import re
import numpy as np
from queue import Queue


class Valve:
    def __init__(self, name, flow_rate=0):
        self.name = name
        self.flow_rate = flow_rate
        self.target_valve_names = []

    def __repr__(self):
        return f"Valve({self.name} flow {self.flow_rate} leads to valves {[v for v in self.target_valve_names]})"


class Bot:
    def __init__(self, distances, valves, valves_index, current_valve_name, current_pressure, released_pressure,
                 open_valves, minutes_left):
        self.distances = distances
        self.valves = valves
        self.valves_index = valves_index
        self.current_valve_name = current_valve_name
        self.current_pressure = current_pressure
        self.released_pressure = released_pressure
        self.open_valves = open_valves
        self.minutes_left = minutes_left
        self.history = []

    def __repr__(self):
        return f"Bot(current_valve={self.current_valve_name} current_pressure={self.current_pressure} " \
               f"released_pressure={self.released_pressure} open_valves={self.open_valves} minutes_left={self.minutes_left})"

    def go_through(self):
        other_bots = []

        if self.minutes_left > 0:
            # Find candidate valves with the following constrains :
            #   should not have been visited, should have a flow rate > 0, should not be the current valve
            # For each occurrence found, we get : (the valve, its distance from the current valve)
            valves_candidates = [(self.valves[ind], self.distances[self.valves_index.index(self.current_valve_name)][
                self.valves_index.index(ind)]) for ind in self.valves_index
                                 if ind not in self.open_valves
                                 and ind != self.current_valve_name
                                 and self.valves[ind].flow_rate > 0]

            # Open the current valve if its flow rate > 0
            if self.valves[self.current_valve_name].flow_rate > 0:
                # This operation takes 1 minute, so increase released_pressure for 1 min
                self.released_pressure += self.current_pressure
                # Update current pressure (add the flow rate of the current valve)
                self.current_pressure += self.valves[self.current_valve_name].flow_rate
                # Decrease the minute counter
                self.minutes_left -= 1

            # Iterate over the candidate valves found
            for vc in valves_candidates:
                valve = vc[0]
                distance = vc[1]

                # The valve should be reachable considering its distance and the minutes left
                if self.minutes_left - distance > 0:
                    # Determine the released pressure we will get when reaching the valve
                    new_released_pressure = self.released_pressure + self.current_pressure * distance

                    # Create a new bot to explore this new path by recursion
                    new_bot = Bot(self.distances, self.valves, self.valves_index, valve.name, self.current_pressure,
                                  new_released_pressure, self.open_valves[:] + [self.current_valve_name],
                                  self.minutes_left - distance)
                    new_bot.history = self.history[:] + [valve.name]

                    other_bots.append(new_bot)

            # This bot won't move anymore, so determine the final released pressure according to the minutes left
            # and return it with the new "children" bots previously created
            return self.released_pressure + self.current_pressure * self.minutes_left, other_bots

        else:
            # If no minute left, simply returns the released pressure, with no bot
            return self.released_pressure, []


def parse_valves(file):
    # Parse values from input file
    valves = {}
    valves_index = []
    with open(file) as f:
        for line in f:
            if m := re.match(r'^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)$',
                             line.strip()):
                # (flow_rate, open_status, [connected vales ...])
                valves[m.group(1)] = Valve(m.group(1), int(m.group(2)))
                valves[m.group(1)].target_valve_names = [x.strip() for x in m.group(3).split(",")]
                valves_index.append(m.group(1))

    return valves, valves_index


def graph_to_matrix(valves, valves_index):
    # Convert valves graph to matrix
    size = len(valves_index)
    matrix = np.ndarray((size, size), dtype=int)
    matrix.fill(0)

    for i, valve_start in enumerate(valves_index):
        for valve_end in valves[valve_start].target_valve_names:
            matrix[i][valves_index.index(valve_end)] = 1

    return matrix


def floyd_warshall(valves, valves_index):
    # Implement the Floyd-Warshall algorithm to get all shortest distance between two nodes
    matrix = graph_to_matrix(valves, valves_index)
    size = len(matrix)

    # Create the distances matrix and fill it with "infinity" value
    # "infinity" is any value that will be higher than the highest possible distance, size * size is such
    # a possible value
    infinity = size * size
    distances = np.ndarray((size, size), dtype=int)
    distances.fill(infinity)

    for i in range(size):
        for j in range(size):
            if i == j:
                distances[i][j] = 0
            elif matrix[i][j] != 0:
                distances[i][j] = matrix[i][j]

    for k in range(size):
        for i in range(size):
            for j in range(size):
                if distances[i][k] + distances[k][j] < distances[i][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]

    # Return the distance matrix, you can find the shortest distance from any valve to any other valve like this:
    # distance_from_valveA_to_valveB = distances[valveA_index][valveB_index]
    return distances


def run(file, part2=False):
    # Get the valve dict from input file and index for converting valve name to index number and vice versa
    # (will be useful for the distance matrix after)
    valves, valves_index = parse_valves(file)
    # Get the distance matrix
    distances = floyd_warshall(valves, valves_index)

    queue = Queue()
    # Create an initial bot that starts at the "AA" valve and put it into a queue
    # This bot will be first go through into the network. Its role is the following:
    #  - duplicate itself (create a "children" bot) for all possible tunnels connected to the valve (under
    #    certain conditions)
    #  - continue without doing anything until the time is exhausted.
    # At the end we note its total released pressure, and the new bots it has generated will be placed into the
    # same queue. We process the other bots by fetching the queue and run them, note their total released pressure
    # until exhaustion of the queue
    starting_bot = Bot(distances, valves, valves_index, "AA", 0, 0, [], 26 if part2 else 30)
    queue.put(starting_bot)

    final_results = []
    while not queue.empty():
        # Get a bot
        bot = queue.get()
        # Run a bot from the queue and get its returns
        released_pressure, other_bots = bot.go_through()

        if part2:
            # For part2, note the released pressure for this bot, put also the valves it has visited
            # from its parent bot
            final_results.append((bot.history, released_pressure))
        else:
            # Note the released pressure for this bot
            final_results.append(released_pressure)

        # If we have other bots, we put them in the queue
        for b in other_bots:
            queue.put(b)

    if part2:
        # For the part2, I considered there is no need to complicate the bot algorithm to simulate the elephant.
        # I assumed that you and the elephant have no influence to each others during your travelling and follow
        # a completely different path. But to have a best released pressure you and the elephant must not have
        # visited same the valve. So my trick is to iterate over all results and inspect their valve path and find
        # all couples of paths that don't have any valve in common in them. These couples are not necessarily the
        # solution but mean that the best released pressure are among them.
        final_results2 = []
        for fr1 in final_results:
            for fr2 in final_results:
                # Compare the valves of the 2 lists, their intersection must be an empty set
                if len(set(fr1[0]) & set(fr2[0])) == 0:
                    # When found, add the 2 released pressures and store the result
                    final_results2.append(fr1[1] + fr2[1])

        # Print the best released pressure
        print(max(final_results2))

    else:
        # Print the best released pressure
        print(max(final_results))


def day16_1(file):
    run(file)


def day16_2(file):
    run(file, part2=True)


if __name__ == '__main__':
    day16_1(sys.argv[1])
    day16_2(sys.argv[1])
