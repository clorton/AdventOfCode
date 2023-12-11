#! /usr/bin/env python3

from collections import defaultdict
from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

space = np.array([list(line) for line in input])

galaxies = []
for y, row in enumerate(space):
    for x, value in enumerate(row):
        if value == "#":
            galaxies.append((x,y))

empty_rows = []
for y, row in enumerate(space):
    if np.all(row == "."):
        empty_rows.append(y)

empty_cols = []
for x, col in enumerate(space.T):
    if np.all(col == "."):
        empty_cols.append(x)

size = np.full(space.shape, 1, dtype=np.uint32)

EXPANSION = 1_000_000  # 2 for part 1, 1_000_000 for part 2

# space[space == "."] = "1"
size[empty_rows,:] = EXPANSION
size[:,empty_cols] = EXPANSION

distances = np.zeros((len(galaxies), len(galaxies)), dtype=np.uint32)

for i, galaxy in enumerate(galaxies):
    gx, gy = galaxy
    for j, other in enumerate(galaxies):

        if j <= i:
            continue

        ox, oy = other

        # horizontal distance
        start, stop = min(gx, ox), max(gx, ox)
        distance = size[gy,start:stop].sum()
        # vertical distance
        start, stop = min(gy, oy), max(gy, oy)
        distance += size[start:stop,gx].sum()

        distances[i,j] = distance

print(f"{distances.sum()=}")

pass
