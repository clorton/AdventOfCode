from pathlib import Path
import re

import numpy as np

with (Path(__file__).parent / "day-05.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

rules = lines[:1176]
updates = lines[1177:]

rules = [tuple(list(map(int, rule.split("|")))) for rule in rules]
updates = [list(map(int, update.split(","))) for update in updates]
# updates = [{value:index for index,value in enumerate(update)} for update in updates]

def check(update, rules):
    lookup = {value:index for index,value in enumerate(update)}
    valid = True
    for p1, p2 in rules:
        if (p1 in lookup) and (p2 in lookup):
            if lookup[p1] > lookup[p2]:
                valid = False
                break
    return valid

total = 0
for update in updates:
    if check(update, rules):
        middle = update[len(update) // 2]
        total += middle

print(f"total = {total}")

def reorder(update, rules):
    reordered = list(update)
    while not check(reordered, rules):
        lookup = {value:index for index,value in enumerate(reordered)}
        for p1, p2 in rules:
            if (p1 in lookup) and (p2 in lookup):
                if lookup[p1] > lookup[p2]:
                    reordered.remove(p1)
                    reordered.insert(lookup[p2], p1)
                    break
    return reordered


total = 0
for update in updates:
    if not check(update, rules):
        fixed = reorder(update, rules)
        middle = fixed[len(fixed) // 2]
        total += middle

print(f"total = {total}")

print("Done.")


