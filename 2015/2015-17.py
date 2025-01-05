import re
from pathlib import Path

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "2015-17.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

containers = sorted([int(line) for line in lines], reverse=True)

capacity = 150

def solve1(containers, amount):
    if amount == 0:
        return 1
    if not containers or amount < 0:
        return 0
    return solve1(containers[1:], amount) + solve1(containers[1:], amount - containers[0])

print(f"Part 1: {solve1(containers, capacity)}")

def solve2(containers, amount, used, options):
    if amount == 0:
        return 1
    if not containers or amount < 0:
        return 0
    remaining = amount - containers[0]
    if (wyth := solve2(containers[1:], remaining, used + 1, options)):
        if remaining not in options:
            options[remaining] = {}
        if used+1 not in options[remaining]:
            options[remaining][used+1] = wyth
        else:
            options[remaining][used+1] += wyth
    if (without := solve2(containers[1:], amount, used, options)):
        if amount not in options:
            options[amount] = {}
        if used not in options[amount]:
            options[amount][used] = without
        else:
            options[amount][used] += without
    return wyth + without

options = {}
solutions = solve2(containers, capacity, 0, options)
print(f"Part 2: {options[0][min(options[0].keys())]}")

print("Done.")
