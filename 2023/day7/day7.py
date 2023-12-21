#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2023/day/7
#

import sys
import re


def get_cards_distribution(l):
    cards_distribution = {}
    for e in l:
        if e not in cards_distribution:
            cards_distribution[e] = 1
        else:
            cards_distribution[e] += 1

    return cards_distribution


def get_cards_counters(l):
    cards_distribution = get_cards_distribution(l)
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
    _CARD_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    _CARD_VALUES_WITH_JOKER = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

    _TYPE_STRENGTH_FIVE_OF_A_KIND = 7
    _TYPE_STRENGTH_FOUR_OF_A_KIND = 6
    _TYPE_STRENGTH_FULL_HOUSE = 5
    _TYPE_STRENGTH_THREE_OF_A_KIND = 4
    _TYPE_STRENGTH_TWO_PAIR = 3
    _TYPE_STRENGTH_ONE_PAIR = 2
    _TYPE_STRENGTH_HIGH_CARD = 1
    _TYPE_STRENGTH_LABELS = ["High card", "One pair", "Two pair", "Three of a kind", "Full House", "Four of a kind", "Five of a kind"]

    def __init__(self, cards, bid, with_joker=False):
        self.cards = cards
        self.bid = bid
        self._with_joker = with_joker
        self._strength = None
        self._pretended_type_strength = None

    def __repr__(self):
        return f"CardHand({self.cards}, {self.bid})"

    def _process_joker(self):
        distribution = get_cards_distribution(self.cards)
        counts = get_cards_counters(self.cards)

        if 'J' in distribution:
            if distribution['J'] == 5:
                self._pretended_type_strength = self._TYPE_STRENGTH_FIVE_OF_A_KIND

            elif distribution['J'] == 4:
                self._pretended_type_strength = self._TYPE_STRENGTH_FOUR_OF_A_KIND

            elif distribution['J'] == 3:
                if 2 in counts:
                    self._pretended_type_strength = self._TYPE_STRENGTH_FULL_HOUSE
                else:
                    self._pretended_type_strength = self._TYPE_STRENGTH_FOUR_OF_A_KIND

            elif distribution['J'] == 2:
                if 3 in counts:
                    self._pretended_type_strength = self._TYPE_STRENGTH_FULL_HOUSE
                elif type(counts[2]) is list:
                    self._pretended_type_strength = self._TYPE_STRENGTH_FOUR_OF_A_KIND
                else:
                    self._pretended_type_strength = self._TYPE_STRENGTH_THREE_OF_A_KIND

            elif distribution['J'] == 1:
                if 4 in counts:
                    self._pretended_type_strength = self._TYPE_STRENGTH_FIVE_OF_A_KIND
                elif 3 in counts:
                    self._pretended_type_strength = self._TYPE_STRENGTH_FOUR_OF_A_KIND
                elif 2 in counts and type(counts[2]) is list:
                    self._pretended_type_strength = self._TYPE_STRENGTH_FULL_HOUSE
                elif 2 in counts and type(counts[2]) is str:
                    self._pretended_type_strength = self._TYPE_STRENGTH_THREE_OF_A_KIND
                else:
                    self._pretended_type_strength = self._TYPE_STRENGTH_ONE_PAIR

            print(f"Joker: {''.join(self.cards)} => {self._TYPE_STRENGTH_LABELS[self._pretended_type_strength - 1]}")

    def _compute_strength(self, cards):
        counts = get_cards_counters(cards)
        type_strength = None

        if self._with_joker:
            cards_values = self._CARD_VALUES_WITH_JOKER
        else:
            cards_values = self._CARD_VALUES

        if not self._pretended_type_strength:
            # Five of a kind, where all five cards have the same label: AAAAA
            if 5 in counts:
                type_strength = self._TYPE_STRENGTH_FIVE_OF_A_KIND

            # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
            elif 4 in counts:
                type_strength = self._TYPE_STRENGTH_FOUR_OF_A_KIND

            # Full house, where three cards have the same label, and the remaining two cards share a
            # different label: 23332
            elif 3 in counts and 2 in counts:
                type_strength = self._TYPE_STRENGTH_FULL_HOUSE

            # Three of a kind, where three cards have the same label, and the remaining two cards are
            # each different from
            # any other card in the hand: TTT98
            elif 3 in counts and 1 in counts:
                type_strength = self._TYPE_STRENGTH_THREE_OF_A_KIND

            # Two pair, where two cards share one label, two other cards share a second label, and the remaining card
            # has a third label: 23432
            elif 2 in counts and type(counts[2]) is list and 1 in counts:
                type_strength = self._TYPE_STRENGTH_TWO_PAIR

            # One pair, where two cards share one label, and the other three cards have a different label from the
            # pair and each other: A23A4
            elif 2 in counts and type(counts[2]) is str and 1 in counts and type(counts[1]) is list:
                type_strength = self._TYPE_STRENGTH_ONE_PAIR

            # High card, where all cards' labels are distinct: 23456
            elif 1 in counts and type(counts[1]) is list and len(counts[1]) == 5:
                type_strength = self._TYPE_STRENGTH_HIGH_CARD

            else:
                print(f"Unknown card hand: {cards}")

        else:
            type_strength = self._pretended_type_strength

        return (
            type_strength,
            cards_values.index(cards[0]),
            cards_values.index(cards[1]),
            cards_values.index(cards[2]),
            cards_values.index(cards[3]),
            cards_values.index(cards[4])
        )

    @property
    def strength(self):
        if not self._strength:
            if self._with_joker:
                self._process_joker()
            self._strength = self._compute_strength(self.cards)

        return self._strength

    @property
    def strength_score(self):
        if not self._strength:
            if self._with_joker:
                self._process_joker()
            self._strength = self._compute_strength(self.cards)

        strength_value = 0
        base = len(self._CARD_VALUES) + 1

        for n in range(len(self._strength)):
            strength_value += base**(len(self._strength) - n) * self._strength[n]

        return strength_value


def parse_card_hands(file, with_joker=False):
    card_hands = []

    with open(file) as f:
        for line in f:
            match = re.search(r"^(\w+)\s+(\d+)$", line.rstrip())

            if match:
                card_hands.append(CardHand([c for c in match.group(1)], int(match.group(2)), with_joker=with_joker))
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
    card_hands = parse_card_hands(file, with_joker=True)
    card_hands_sorted = sorted(card_hands, key=lambda ch: ch.strength_score)

    total_winnings = 0

    for n in range(len(card_hands_sorted)):
        ch = card_hands_sorted[n]
        total_winnings += (n + 1) * ch.bid

        print(ch, ch.strength, ch.strength_score)

    print(total_winnings)


if __name__ == '__main__':
    #day7_1(sys.argv[1])
    day7_2(sys.argv[1])

