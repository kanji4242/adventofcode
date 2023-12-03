#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/2
#

import sys
import re

GAME_RED_CUBES = 12
GAME_GREEN_CUBES = 13
GAME_BLUE_CUBES = 14


def parse_games(file):
    games = {}

    with open(file) as f:
        for line in f:
            line = line.rstrip()
            line = line.replace(";", ",")

            # Match the line format and try to find the match in the line
            match = re.search(r"Game (\d+): (.+)", line)

            if match:
                game_id = int(match.group(1))

                color_datas = match.group(2).split(',')

                color_revelations = []

                for cube in color_datas:
                    # Extract individual color and value
                    color_match = re.search(r"(\d+) (blue|red|green)", cube)

                    if color_match:
                        value = int(color_match.group(1))
                        color = color_match.group(2)

                        # Add color and value to the list
                        color_revelations.append((color, value))

                # Add the game to the dict
                games[game_id] = color_revelations
            else:
                print(f"No match found for line: {line}")

    return games


def find_impossible_games(games: dict):
    result = 0

    for game_id, color_revelations in games.items():
        game_impossible = False
        for color_revel in color_revelations:
            # Review all the colors and find if this is possible by comparing the number revealed to the
            # initial game setup.
            if color_revel[0] == 'red' and color_revel[1] > GAME_RED_CUBES:
                game_impossible = True
            if color_revel[0] == 'green' and color_revel[1] > GAME_GREEN_CUBES:
                game_impossible = True
            if color_revel[0] == 'blue' and color_revel[1] > GAME_BLUE_CUBES:
                game_impossible = True

        if not game_impossible:
            result += game_id

    return result


def find_fewest_nb_of_cubes(games):
    result = 0

    for game_id, color_revelations in games.items():
        # Find the max value revealed for each color, this will give us the fewest number of cubes of each of them
        fewest_red_cubes = max([color_revel[1] for color_revel in color_revelations if color_revel[0] == 'red'])
        fewest_green_cubes = max([color_revel[1] for color_revel in color_revelations if color_revel[0] == 'green'])
        fewest_blue_cubes = max([color_revel[1] for color_revel in color_revelations if color_revel[0] == 'blue'])
        result += fewest_red_cubes * fewest_green_cubes * fewest_blue_cubes

    return result

def day2_1(file):
    print(find_impossible_games(parse_games(file)))


def day2_2(file):
    print(find_fewest_nb_of_cubes(parse_games(file)))


if __name__ == '__main__':
    day2_1(sys.argv[1])
    day2_2(sys.argv[1])

