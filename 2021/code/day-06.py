#! /usr/bin/env python3

from collections import Counter
from pathlib import Path

import numpy as np

with Path("../inputs/06.txt").open("r") as handle:
    lines = list([line.strip() for line in handle.readlines()])

timers = list(map(int, lines[0].split(",")))
counter = Counter(timers)

# counter = {1: 1, 2: 1, 3: 2, 4: 1}

population = np.zeros(9, dtype=np.uint64)
for key, value in counter.items():
    population[key] = value

for day in range(80):
    update = np.zeros(9, dtype=np.uint64)
    for timer in range(9):
        if timer == 0:
            update[8] += population[timer]  # new fish
            update[6] += population[timer]  # reset timer
        else:
            update[timer-1] += population[timer]
    population[:] = update[:]

total = np.sum(population)
print(f"After 80 days, {total=}")

population = np.zeros(9, dtype=np.uint64)
for key, value in counter.items():
    population[key] = value

for day in range(256):
    update = np.zeros(9, dtype=np.uint64)
    for timer in range(9):
        if timer == 0:
            update[8] += population[timer]  # new fish
            update[6] += population[timer]  # reset timer
        else:
            update[timer-1] += population[timer]
    population[:] = update[:]

total = np.sum(population)
print(f"After 256 days, {total=}")


pass
