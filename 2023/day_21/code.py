#! /usr/bin/env python3

from collections import defaultdict
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
count, filename = 6, "example.txt"
# count, filename = 64, "input.txt"
INPUT_FILE = Path(__file__).parent / filename

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

garden = np.array([list(line) for line in input])

startx = -1
starty = -1
for row in range(garden.shape[0]):
    for col in range(garden.shape[1]):
        if garden[row, col] == "S":
            startx, starty = col, row
            garden[row, col] = "."
        # if garden[row, col] == ".":
        #     garden[row, col] = 0
        # elif garden[row, col] == "#":
        #     garden[row, col] = 1

paths = np.full_like(garden, -1, dtype=np.int8)
paths[starty, startx] = 0
for step in tqdm(range(count)):
    places = np.nonzero(paths == step)
    for y, x in zip(*places):
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if garden[y + dy, x + dx] == ".":   # and paths[y + dy, x + dx] == -1:
                paths[y + dy, x + dx] = step + 1

print(f"Part 1: {np.sum(paths == (count))=}")

pass
