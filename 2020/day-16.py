#! /usr/bin/env python3

from collections import deque, namedtuple
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-16.txt").read_text()

# text = """class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19
#
# your ticket:
# 11,12,13
#
# nearby tickets:
# 3,9,18
# 15,1,5
# 5,14,9"""

sections = text.split("\n\n")
rules = sections[0].split("\n")
mine = sections[1].split("\n")[-1]
mine = [int(data) for data in mine.split(",")]
nearby = sections[2].split("\n")[1:]
nearby = [[int(data) for data in ticket.split(",")] for ticket in nearby]
# numbers = [int(string) for string in lines]


# part 1
def parse_rule(rule):
    rule = rule.split(": ")
    name = rule[0]
    ranges = rule[1].split(" or ")
    first = ranges[0].split("-")
    second = ranges[1].split("-")
    return name, (int(first[0]), int(first[1])), (int(second[0]), int(second[1]))


rules = [parse_rule(rule) for rule in rules]

valid = set()
for rule in rules:
    valid.update(range(rule[1][0], rule[1][1]))
    valid.update(range(rule[2][0], rule[2][1]))

total = 0
invalid = set()
for index, ticket in enumerate(nearby):
    for value in ticket:    # [int(data) for data in ticket.split(",")]:
        if value not in valid:
            total += value
            invalid.update([index])

print(f"Total of invalid values is {total}.")

# part 2
ranges = {}
for rule in rules:
    valid = set()
    valid.update(range(rule[1][0], rule[1][1]+1))
    valid.update(range(rule[2][0], rule[2][1]+1))
    ranges[rule[0]] = valid

columns = [set(ranges.keys()) for _ in range(len(mine))]

for it, ticket in enumerate(nearby):
    if it not in invalid:
        for iv, value in enumerate(ticket):
            valid = set()
            for datum, values in ranges.items():
                if value in values:
                    valid.update([datum])
            columns[iv] &= valid

ordered = [(index, column) for index, column in enumerate(columns)]
ordered.sort(key=lambda t: len(t[1]))
for index, (ia, column) in enumerate(ordered):
    for ib, other in ordered[index+1:]:
        columns[ib] -= columns[ia]

product = 1
for index, column in enumerate(columns):
    if list(column)[0].startswith("departure"):
        product *= mine[index]

print(f"Product of departure columns is {product}.")

print(".oO( done )")
