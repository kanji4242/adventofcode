#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2022/day/21
#

"""
I don't use object for this one. The idea is to create a dict containing all monkeys. The key of the dict is its name,
and the value of the dist depends on the type of monkey :
 - if we have a yell monkey, it will simply be an int with the number it yells
 - if we have an operator monkey, it will be a tuple with 3 values : the waiting monkey #1, the operation, and the
   waiting monkey #2

For instance, if we have the following monkeys :
cczh: sllz + lgvd
zczc: 2

The generated dict will look like this :
{
  'cczh': ("sllz",  '+',  "lgvd"),
  'zczc': 2
}

For the part 1, we simply iterate over all monkeys we got, and detect an operator monkey which has 2 yell monkeys, then
we simply transform it into a yell monkey. That is, we change the value of that monkey to an int with the result of its
operation. We repeat this iteration process forever until the "root" monkey became a yell monkey (i.e. its value is not
a tuple).

For the part 2, the idea is to force the operation of the "root" monkey to be a subtraction ('-'). Since we expect
the 2 waiting monkeys to yell the same number, the "root" monkey will then yell the number 0.
This will be helpful to determine the number to adjust for the "humn" monkey, thanks to the use of the bisection
method.
"""

import sys


def read_monkeys(file):
    monkeys = {}
    with open(file) as f:
        for line in f:
            line = line.strip()
            name = line[:line.find(":")]
            job = line[line.find(":"):].replace(': ', '')
            # If the right side is an integer, it's a yell monkey
            if job.isdigit():
                # We set an int with the number it yells
                monkeys[name] = int(job)
            else:
                # We set a tuple with the 3 values
                monkeys[name] = tuple(job.split(" "))

    return monkeys


def process_monkeys(monkeys_ref, humn_value=None):
    monkeys = monkeys_ref.copy()

    # We can adjust the yell number of the "humn" monkey (part 2 only)
    if humn_value:
        monkeys['humn'] = humn_value

    # Iterate over all monkeys while the "root" monkey is still an operator mnkey
    while type(monkeys['root']) is tuple:
        for name, operation in monkeys.items():
            # Detect an operator monkey which has 2 yell monkeys
            if type(operation) is tuple \
                    and type(monkeys[operation[0]]) is int and type(monkeys[operation[2]]) is int:
                result = None
                # Perform the operation
                if operation[1] == '+':
                    result = monkeys[operation[0]] + monkeys[operation[2]]
                if operation[1] == '-':
                    result = monkeys[operation[0]] - monkeys[operation[2]]
                if operation[1] == '*':
                    result = monkeys[operation[0]] * monkeys[operation[2]]
                if operation[1] == '/':
                    result = monkeys[operation[0]] // monkeys[operation[2]]
                monkeys[name] = result

    return monkeys["root"]


def find_humn_by_bisection(monkeys):
    # We force the operation of the "root" monkey to be subtraction so that the "root" monkey will yell the number 0.
    monkeys["root"] = (monkeys["root"][0], "-", monkeys["root"][2])

    # We do a first run with no adjustment of the "humn" monkey
    diff = process_monkeys(monkeys)

    # If the result number is negative, we invert the 2 monkey to always get a positive number
    if diff < 0:
        monkeys["root"] = (monkeys["root"][2], "-", monkeys["root"][0])
        diff = -diff

    # We start adjusting the "humn" monkey by iteration until we get a negative result
    # We don't know how much to adjust, the number can be very large, to optimize we proceed in logarithmic way
    # by multiply by 10 each step.
    adjustment = 1
    while diff > 0:
        adjustment *= 10
        diff = process_monkeys(monkeys, humn_value=adjustment)

    # The real bisection method begins here:
    # our interval A is the last adjustment we had when the result was still positive (we get it by dividing by 10)
    # our interval B is simply the last adjustment we got previously
    interval_a = adjustment // 10
    interval_b = adjustment
    while True:
        # Compute the midpoint of the 2 intervals
        result = (interval_a + interval_b) // 2
        diff = process_monkeys(monkeys, humn_value=result)
        # Adjust the interval A or interval B depending on the result
        if diff > 0:
            interval_a = result
        elif diff < 0:
            interval_b = result
        else:
            # If the result is 0, we are done
            break

    return result


def display_monkeys(monkeys):
    # For debugging purpose only
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
    print(find_humn_by_bisection(monkeys))


if __name__ == '__main__':
    day21_1(sys.argv[1])
    day21_2(sys.argv[1])
