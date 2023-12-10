#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/7
#

import sys
import re


def count_cards(l):
    cards_distribution = {}
    for e in l:
        if e not in cards_distribution:
            cards_distribution[e] = 1
        else:
            cards_distribution[e] += 1

    cards_count = {}
    for k, v in cards_distribution.items():
        if v not in cards_count:
            cards_count[v] = k
        elif type(cards_count[v]) is str:
            cards_count[v] = [cards_count[v], k]
        else:
            cards_count[v].append(k)

    return cards_count


class CardHand:
    _card_values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid
        self._strength = None

    def __repr__(self):
        return f"CardHand({self.cards}, {self.bid})"

    def _compute_strength(self):
        counts = count_cards(self.cards)
        type_strength = None

        # Five of a kind, where all five cards have the same label: AAAAA
        if 5 in counts:
            type_strength = 7

        # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        elif 4 in counts:
            type_strength = 6

        # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        elif 3 in counts and 2 in counts:
            type_strength = 5

        # Three of a kind, where three cards have the same label, and the remaining two cards are each different from
        # any other card in the hand: TTT98
        elif 3 in counts and 1 in counts:
            type_strength = 4

        # Two pair, where two cards share one label, two other cards share a second label, and the remaining card
        # has a third label: 23432
        elif 2 in counts and type(counts[2]) is list and 1 in counts:
            type_strength = 3

        # One pair, where two cards share one label, and the other three cards have a different label from the
        # pair and each other: A23A4
        elif 2 in counts and type(counts[2]) is str and 1 in counts and type(counts[1]) is list:
            type_strength = 2

        # High card, where all cards' labels are distinct: 23456
        elif 1 in counts and type(counts[1]) is list and len(counts[1]) == 5:
            type_strength = 1

        else:
            print(f"Unknown card hand: {self.cards}")

        self._strength = (
            type_strength,
            self._card_values.index(self.cards[0]),
            self._card_values.index(self.cards[1]),
            self._card_values.index(self.cards[2]),
            self._card_values.index(self.cards[3]),
            self._card_values.index(self.cards[4])
        )

    @property
    def strength(self):
        if not self._strength:
            self._compute_strength()

        return self._strength

    @property
    def strength_score(self):
        if not self._strength:
            self._compute_strength()

        strength_value = 0
        base = len(self._card_values) + 1

        for n in range(len(self._strength)):
            strength_value += base**(len(self._strength) - n) * self._strength[n]

        return strength_value


def parse_card_hands(file):
    card_hands = []

    with open(file) as f:
        for line in f:
            match = re.search(r"^(\w+)\s+(\d+)$", line.rstrip())

            if match:
                card_hands.append(CardHand([c for c in match.group(1)], int(match.group(2))))
            else:
                print(f"No match found for line: {line}")

    return card_hands


def day7_1(file):
    card_hands = parse_card_hands(file)
    card_hands_sorted = sorted(card_hands, key=lambda ch: ch.strength_score)

    total_winnings = 0

    for n in range(len(card_hands_sorted)):
        ch = card_hands_sorted[n]
        total_winnings += (n + 1) * ch.bid

        print(ch, ch.strength, ch.strength_score)

    print(total_winnings)


def day7_2(file):
    print(parse_card_hands(file))


if __name__ == '__main__':
    day7_1(sys.argv[1])
    #day7_2(sys.argv[1])

