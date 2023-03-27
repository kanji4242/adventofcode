#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/11
#

import sys
from functools import reduce


class Item:
    def __init__(self, worry_level):
        self.worry_level = worry_level

    def __repr__(self):
        return f"Item({self.worry_level})"


class Monkey:
    def __init__(self, monkey_id, items, operation, worry_test, throw_worry_if_true, throw_worry_if_false, is_bored):
        self.monkey_id = monkey_id
        self.items = items
        self.operation = operation
        self.worry_test = worry_test
        self.throw_worry_if_true = throw_worry_if_true
        self.throw_worry_if_false = throw_worry_if_false
        self.monkey_throw_worry_if_true = None
        self.monkey_throw_worry_if_false = None
        self.is_bored = is_bored
        self.fix_worry = None
        self.inspected = 0

    def __repr__(self):
        return f"Monkey({repr(self.items)}, {self.operation}, {self.worry_test}, " \
               f"{self.throw_worry_if_true}, {self.throw_worry_if_false})"

    def inspect(self):
        for item in self.items:
            self.inspected += 1

            if self.fix_worry:
                item.worry_level = item.worry_level % self.fix_worry

            item.worry_level = int(eval(self.operation.format(item=item.worry_level)))
            if self.is_bored:
                item.worry_level = int(item.worry_level / 3)

            if item.worry_level % self.worry_test == 0:
                self.monkey_throw_worry_if_true.items.append(item)
            else:
                self.monkey_throw_worry_if_false.items.append(item)
        self.items.clear()


def parse_monkeys(file, with_boring=True):
    monkeys = []
    with open(file) as f:
        while line := f.readline():
            line = line.strip()
            if line.startswith("Monkey "):
                monkey_id, starting_items, operation = int(line[7:-1]), [], ""
                worry_test = throw_worry_if_true = 0

                while line := f.readline():
                    line = line.strip()
                    if line.startswith("Starting items: "):
                        for item in line[16:].split(","):
                            starting_items.append(Item(int(item.strip())))
                    elif line.startswith("Operation: new = "):
                        operation = line[17:].replace("old", "{item}")
                    elif line.startswith("Test: divisible by "):
                        worry_test = int(line[19:])
                    elif line.startswith("If true: throw to monkey "):
                        throw_worry_if_true = int(line[25:])
                    elif line.startswith("If false: throw to monkey "):
                        throw_worry_if_false = int(line[26:])
                        monkeys.append(Monkey(monkey_id, starting_items, operation, worry_test,
                                              throw_worry_if_true, throw_worry_if_false, with_boring))
                    else:
                        break

    for monkey in monkeys:
        monkey.monkey_throw_worry_if_true =\
            [m for m in monkeys if m.monkey_id == monkey.throw_worry_if_true][0]
        monkey.monkey_throw_worry_if_false = \
            [m for m in monkeys if m.monkey_id == monkey.throw_worry_if_false][0]

    return monkeys


def day11_1(file):
    monkeys = parse_monkeys(file, with_boring=True)

    for _ in range(20):
        for monkey in monkeys:
            monkey.inspect()

    print(reduce((lambda x, y: x * y), sorted([m.inspected for m in monkeys], reverse=True)[:2]))


def day11_2(file):
    monkeys = parse_monkeys(file, with_boring=False)

    fix_worry = reduce((lambda x, y: x * y), [m.worry_test for m in monkeys])
    for monkey in monkeys:
        monkey.fix_worry = fix_worry

    for _ in range(10000):
        for monkey in monkeys:
            monkey.inspect()

    print(reduce((lambda x, y: x * y), sorted([m.inspected for m in monkeys], reverse=True)[:2]))


if __name__ == '__main__':
    day11_1(sys.argv[1])
    day11_2(sys.argv[1])

