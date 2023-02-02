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
            # For each occurrence found, we get : (the valve, the distance from current valve)
            valves_candidates = [(self.valves[ind], self.distances[self.valves_index.index(self.current_valve_name)][
                self.valves_index.index(ind)]) for ind in self.valves_index
                                 if ind not in self.open_valves
                                 and ind != self.current_valve_name
                                 and self.valves[ind].flow_rate > 0]

            # Open the valve if its flow rate > 0
            if self.valves[self.current_valve_name].flow_rate > 0:
                # This operation takes 1 minute, so increase released_pressure for 1 min
                self.released_pressure += self.current_pressure
                # Update current_pressure (add the current flow rate)
                self.current_pressure += self.valves[self.current_valve_name].flow_rate
                # Decrease minute counter
                self.minutes_left -= 1

            # Iterate over candidate valves
            for vc in valves_candidates:
                valve = vc[0]
                distance = vc[1]

                # The valve should be reachable considering its distance and the minutes left
                if self.minutes_left - distance > 0:
                    # Determine the released pressure when reaching the valve
                    new_released_pressure = self.released_pressure + self.current_pressure * distance

                    # Create a new bot to explore this new path by recursion
                    new_bot = Bot(self.distances, self.valves, self.valves_index, valve.name, self.current_pressure,
                                  new_released_pressure, self.open_valves[:] + [self.current_valve_name],
                                  self.minutes_left - distance)
                    new_bot.history = self.history[:] + [valve.name]

                    other_bots.append(new_bot)

            # This bot won't move anymore, so determine the final released pressure according to the minutes left
            # and return it with the new bots previously created
            return self.released_pressure + self.current_pressure * self.minutes_left, other_bots

        else:
            # If no minute left, simply returns the released pressure
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
    # Implement the Floyd-Warshall algorithm to find all shortest paths between two nodes
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

    # Return the distances matrix, you can find the distance from any valve to any other valve like this:
    # distance = distances[start_valve_index][end_valve_index]
    return distances


def day16_1(file):
    # Get the valve dict from input file and index for converting valve name to index number and vice versa
    # (will be useful for the distances matrix after)
    valves, valves_index = parse_valves(file)
    print(valves, valves_index)
    distances = floyd_warshall(valves, valves_index)
    print(distances)

    queue = Queue()
    # Create initial bot that starts at "AA" valve
    starting_bot = Bot(distances, valves, valves_index, "AA", 0, 0, [], 30)
    queue.put(starting_bot)

    final_results = []
    while not queue.empty():
        bot = queue.get()
        # Run a bot from the queue and get its returns
        released_pressure, other_bots = bot.go_through()

        # Add the released pressure for this bot
        final_results.append(released_pressure)

        # If we have other bots, put them in the queue
        for b in other_bots:
            queue.put(b)

    # Print the best released pressure
    print(max(sorted(final_results, reverse=True)))


def day16_2(file):
    # Get the valve dict from input file and index for converting valve name to index number and vice versa
    valves, valves_index = parse_valves(file)
    print(valves, valves_index)
    distances = floyd_warshall(valves, valves_index)
    print(distances)

    queue = Queue()
    # Create initial bot that starts at "AA" valve
    starting_bot = Bot(distances, valves, valves_index, "AA", 0, 0, [], 26)
    queue.put(starting_bot)

    final_results = []
    while not queue.empty():
        bot = queue.get()
        # Run the bot and get its returns
        released_pressure, other_bots = bot.go_through()

        # Add the released pressure for this bot
        # We also get the visited valves path available from the history
        final_results.append((bot.history, released_pressure))

        # If we have other bots, put them in the queue
        for b in other_bots:
            queue.put(b)

    # Compare all couples of 2 paths and find the ones that don't have any valve in common in them
    final_results2 = []
    for fr1 in final_results:
        for fr2 in final_results:
            if len(set(fr1[0]) & set(fr2[0])) == 0:
                final_results2.append(fr1[1] + fr2[1])
                # When found, add the 2 released pressures and store the result
                if fr1[1] + fr2[1] == 2031:
                    print(fr1, fr2)

    # Print the best released pressure
    print(max(final_results2))


if __name__ == '__main__':
    day16_1(sys.argv[1])
    day16_2(sys.argv[1])
