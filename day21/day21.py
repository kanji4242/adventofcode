#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/21
#

import sys


def read_monkeys(file):
    monkeys = {}
    with open(file) as f:
        for line in f:
            line = line.strip()
            name = line[:line.find(":")]
            job = line[line.find(":"):].replace(': ', '')
            if job.isdigit():
                monkeys[name] = int(job)
            else:
                monkeys[name] = tuple(job.split(" "))

    return monkeys


def process_monkeys(monkeys_ref, humn_value=None):
    monkeys = monkeys_ref.copy()
    if humn_value:
        monkeys['humn'] = humn_value

    while type(monkeys['root']) is tuple:
        for name, operation in monkeys.items():
            if type(operation) is tuple \
                    and type(monkeys[operation[0]]) is int and type(monkeys[operation[2]]) is int:
                result = None
                if operation[1] == '+':
                    result = monkeys[operation[0]] + monkeys[operation[2]]
                if operation[1] == '-':
                    result = monkeys[operation[0]] - monkeys[operation[2]]
                if operation[1] == '*':
                    result = monkeys[operation[0]] * monkeys[operation[2]]
                if operation[1] == '/':
                    result = int(monkeys[operation[0]] / monkeys[operation[2]])
                monkeys[name] = result

    return monkeys["root"]


def find_humn_by_bisection(monkeys):
    diff = process_monkeys(monkeys)
    if diff < 0:
        monkeys["root"] = (monkeys["root"][2], "-", monkeys["root"][0])
        diff = -diff

    increment = 1
    while diff > 0:
        increment *= 10
        diff = process_monkeys(monkeys, humn_value=increment)

    increment_a = int(increment / 10)
    increment_b = increment
    while True:
        result = int((increment_a + increment_b) / 2)
        diff = process_monkeys(monkeys, humn_value=result)
        if diff > 0:
            increment_a = result
        elif diff < 0:
            increment_b = result
        else:
            break

    return result


def display_monkeys(monkeys):
    print("---")
    for name, operation in monkeys.items():
        if type(operation) is int:
            print(f"{name}: {operation}")
        elif type(operation) is tuple:
            print(f"{name}: {operation[0]} {operation[1]} {operation[2]}")
    print("---")


def day21_1(file):
    monkeys = read_monkeys(file)
    print(process_monkeys(monkeys))


def day21_2(file):
    monkeys = read_monkeys(file)
    monkeys["root"] = (monkeys["root"][0], "-", monkeys["root"][2])
    print(find_humn_by_bisection(monkeys))


if __name__ == '__main__':
    day21_1(sys.argv[1])
    day21_2(sys.argv[1])
