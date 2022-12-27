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
    def __init__(self, monkey_id, items, operation, worry_test, throw_worry_if_true, throw_worry_if_false):
        self.monkey_id = monkey_id
        self.items = items
        self.operation = operation
        self.worry_test = worry_test
        self.throw_worry_if_true = throw_worry_if_true
        self.throw_worry_if_false = throw_worry_if_false
        self.monkey_throw_worry_if_true = None
        self.monkey_throw_worry_if_false = None
        self.inspected = 0

        self.correction = eval(self.operation.format(item=0)) % self.worry_test

    def __repr__(self):
        return f"Monkey({repr(self.items)}, {self.operation}, {self.worry_test}, " \
               f"{self.throw_worry_if_true}, {self.throw_worry_if_false})"

    def inspect(self):
        for item in self.items:
            print("inspect", item.worry_level)
            self.inspected += 1
            item.worry_level = int(eval(self.operation.format(item=item.worry_level)) / 3)

            if item.worry_level % self.worry_test == 0:
                self.monkey_throw_worry_if_true.items.append(item)
            else:
                self.monkey_throw_worry_if_false.items.append(item)
        self.items.clear()

    def inspect2(self):
        print("-monkey", self.monkey_id, self.correction)
        for item in self.items:
            print("inspect", item.worry_level)
            #item.worry_level = (self.worry_test - self.correction) % self.worry_test
            #print("inspect new", item.worry_level)
            self.inspected += 1
            item.worry_level = eval(self.operation.format(item=item.worry_level))
            #print("inspect new", item.worry_level, "modulo =", item.worry_level % self.worry_test)

            if item.worry_level % self.worry_test == 0:
                test1 = eval(self.monkey_throw_worry_if_true.operation.format(item=item.worry_level)) % self.monkey_throw_worry_if_true.worry_test
                item.worry_level = item.worry_level % self.monkey_throw_worry_if_true.worry_test
                test2 = eval(self.monkey_throw_worry_if_true.operation.format(item=item.worry_level)) % self.monkey_throw_worry_if_true.worry_test
                print("diff", test1, test2)
                print("throw to", self.monkey_throw_worry_if_true.monkey_id, item.worry_level)
                self.monkey_throw_worry_if_true.items.append(item)
            else:
                test1 = eval(self.monkey_throw_worry_if_false.operation.format(item=item.worry_level)) % self.monkey_throw_worry_if_false.worry_test
                item.worry_level = item.worry_level % self.monkey_throw_worry_if_false.worry_test
                test2 = eval(self.monkey_throw_worry_if_false.operation.format(item=item.worry_level)) % self.monkey_throw_worry_if_false.worry_test
                print("diff", test1, test2)
                print("throw to", self.monkey_throw_worry_if_false.monkey_id, item.worry_level)
                self.monkey_throw_worry_if_false.items.append(item)
        self.items.clear()


def parse_monkeys(file):
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
                                              throw_worry_if_true, throw_worry_if_false))
                    else:
                        break

    for monkey in monkeys:
        monkey.monkey_throw_worry_if_true =\
            [m for m in monkeys if m.monkey_id == monkey.throw_worry_if_true][0]
        monkey.monkey_throw_worry_if_false = \
            [m for m in monkeys if m.monkey_id == monkey.throw_worry_if_false][0]

    return monkeys


def day11_1(file):
    monkeys = parse_monkeys(file)

    for _ in range(20):
        for monkey in monkeys:
            monkey.inspect()

    print(reduce((lambda x, y: x * y), sorted([m.inspected for m in monkeys], reverse=True)[:2]))


def day11_2(file):
    monkeys = parse_monkeys(file)

    for _ in range(20):
        print(f"--round{_}---")
        for monkey in monkeys:
            monkey.inspect2()
        for monkey in monkeys:
            print(f"{monkey.monkey_id}:", ", ".join([str(item.worry_level) for item in monkey.items]))

        print([m.inspected for m in monkeys])

    print(reduce((lambda x, y: x * y), sorted([m.inspected for m in monkeys], reverse=True)[:2]))


if __name__ == '__main__':
    #day11_1(sys.argv[1])
    day11_2(sys.argv[1])

