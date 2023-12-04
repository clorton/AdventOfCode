#! /usr/bin/env python3

from collections import defaultdict
from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

input = [line.split(": ") for line in input]
input = [ [a.split()[1]] + b.split(" | ") for a,b in input ]
input = [ [a, list(map(int, b.split())), list(map(int, c.split()))] for a, b, c in input]

total = 0
for card, winning, numbers in input:
    w = set(winning)
    winners = list(filter(lambda n: n in w, numbers))
    if len(winners):    # > 0
        value = 1 << (len(winners) - 1)
        total += value

print(f"{total=}")

counts = np.ones(len(input), dtype=np.uint32)
counts[0] = 1
for index, (_, winning, numbers) in enumerate(input):
    w = set(winning)
    winners = list(filter(lambda n: n in w, numbers))
    c = counts[index]
    for jndex in range(index+1, index+1+len(winners)):
        counts[jndex] += c

print(f"{sum(counts)=}")

pass