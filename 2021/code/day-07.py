#! /usr/bin/env python3
import sys
from pathlib import Path

import numpy as np

with Path("../inputs/07.txt").open("r") as handle:
    lines = [line.strip() for line in handle.readlines()]

positions = np.array(list(map(int, lines[0].split(","))), dtype=np.int64)

# positions = np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14], dtype=np.int64)

minimum = sys.maxsize
for position in range(min(positions), max(positions)+1):
    fuel = np.sum(np.abs(positions - position))
    if fuel < minimum:
        minimum = fuel

print(f"Part 1: {minimum=}")

minimum = sys.maxsize
for position in range(min(positions), max(positions)+1):
    distance = np.abs(positions - position)
    cost = distance * (distance + 1) // 2
    fuel = np.sum(cost)
    if fuel < minimum:
        minimum = fuel

print(f"Part 2: {minimum=}")

pass
