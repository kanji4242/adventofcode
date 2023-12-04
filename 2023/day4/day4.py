#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/4
#

import sys
import re


def parse_cards(file):
    # Parse the input file and return a dict containing all the cards with their ID and their number of
    # matching numbers
    cards = {}

    with open(file) as f:
        for line in f:
            # Match the game format
            match = re.search(r"Card\s+(\d+):(.+\|.+)", line)

            if match:
                # Extract the card ID
                card_id = int(match.group(1))

                # Extract the two lists of numbers
                winning_numbers = match.group(2).split('|')[0].strip().split()
                numbers_i_have = match.group(2).split('|')[1].strip().split()

                # Find the common numbers
                matching_numbers = set(map(int, winning_numbers)).intersection(set(map(int, numbers_i_have)))

                # Write the number of matching numbers in the cards dict
                cards[card_id] = len(matching_numbers)

            else:
                print(f"No match found for line: {line}")

    return cards


def find_total_points(cards):
    total_points = 0

    # We don't need the card ID for this part, only the numbers of matching numbers
    for nb_of_matches in cards.values():
        if nb_of_matches:
            # For every card that has matching numbers, since a card gives one point, and we double (multiply by 2)
            # the points for each match, this is similar to set the number 2 raised to power of the numbers of
            # matches minus 1
            total_points += 2 ** (nb_of_matches - 1)

    return total_points


def find_total_scratchcards(cards):
    i = 0

    # At then begin, we have all our cards. Set them in a pool of cards list
    cards_pool = list(cards.keys())

    # Inspect every card anf their matching numbers, if they have matching numbers we append more cards to the list
    while i < len(cards_pool):
        if cards_pool[i] in cards:
            for n in range(cards[cards_pool[i]]):
                # The added cards are the cards below the winning card equal to the number of matches
                cards_pool.append(cards_pool[i] + n + 1)
        i += 1

    return len(cards_pool)


def day4_1(file):
    print(find_total_points(parse_cards(file)))


def day4_2(file):
    print(find_total_scratchcards(parse_cards(file)))


if __name__ == '__main__':
    day4_1(sys.argv[1])
    day4_2(sys.argv[1])

