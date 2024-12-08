#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://adventofcode.com/2024/day/5
#

import sys
import re


class Page:
    def __init__(self, number):
        self.number = number  # Identifying the page
        self.successors = []  # A list to hold successor pages (connections)

    def __repr__(self):
        successors = ','.join([repr(p) for p in self.successors])
        return f"Page({self.number}, [{successors}])"

    def find_successor(self, number):
        for page in self.successors:
            if page.number == number:
                return page


def find_page(pages, number):
    for page in pages:
        if page.number == number:
            return page


# Parse an ordering rule
def parse_page_ordering_rule(pages, line):
    # Extract two page numbers from the input line
    m = re.search(r'^(\d+)\|(\d+)$', line)

    # Find the pages corresponding to the extracted numbers
    page = find_page(pages, m.group(1))
    page_s = find_page(pages, m.group(2))

    # If the first page doesn't exist in the list, create it and add it
    if not page:
        page = Page(m.group(1))
        # Add the new page to the pages list
        pages.append(page)

    # If the second page doesn't exist in the list, create it and add it
    if not page_s:
        page_s = Page(m.group(2))
        # Add the new page to the pages list
        pages.append(page_s)

    # Add the second page as a successor of the first page
    page.successors.append(page_s)


# Process an update represented as a series of page numbers and return the middle page number
def parse_update(pages, steps):
    # Find the initial page (starting point) in the list of pages
    current_page = find_page(pages, steps[0])

    # If the starting page exists
    if current_page:
        # Traverse through the steps to follow successors
        # Iterate over all steps except the first
        for step in steps[1:]:
            # Find the successor page corresponding to the current step
            new_page = current_page.find_successor(step)

            # If the successor exists, move to the next page
            if new_page:
                current_page = new_page
            else:
                # If a step points to a nonexistent page, return 0
                return 0

    # If traversal is successful, return the middle page number
    return int(steps[len(steps) // 2])


# Process an incorrect update represented as a series of page numbers and return the middle page number
def parse_incorrect_update(pages, steps):
    # Loop to repeatedly process and correct the sequence of steps until update is correct
    while parse_update(pages, steps) == 0:  # Continue while `parse_update` returns 0 (invalid path)
        # Iterate through the steps to check and adjust their order
        for i in range(len(steps) - 1):
            # Check if the next step corresponds to an existing page and
            # if the next step's page has a successor pointing back to the current step
            if page := find_page(pages, steps[i + 1]):
                if page.find_successor(steps[i]):
                    # Swap the two steps to correct their order
                    steps[i + 1], steps[i] = steps[i], steps[i + 1]

    # Once the loop exits (the update is now correct), return the middle page number
    return int(steps[len(steps) // 2])


def parse_file(file, part2=False):
    pages = []
    result = 0

    with open(file) as f:
        for line in f:
            line = line.strip()
            if line.find("|") > 0:
                parse_page_ordering_rule(pages, line)

            elif line.find(",") > 0:
                # Split the input line into page steps using a comma as the delimiter
                steps = line.split(',')

                if not part2:
                    result += parse_update(pages, steps)
                else:
                    middle_page_number = parse_update(pages, steps)
                    if middle_page_number == 0:
                        result += parse_incorrect_update(pages, steps)

    print(result)


def day5_1(file):
    parse_file(file)


def day5_2(file):
    parse_file(file, part2=True)


if __name__ == '__main__':
    day5_1(sys.argv[1])
    day5_2(sys.argv[1])
