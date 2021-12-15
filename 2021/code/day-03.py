#! /usr/bin/env python3

from pathlib import Path
import numpy as np

with Path("../inputs/03.txt").open("r") as handle:
    lines = handle.readlines()

values = list(map(lambda s: [int(b) for b in s.strip()], lines))
data = np.array(values)

rows, columns = data.shape

gamma = ''
epsilon = ''
for column in range(columns):
    print(f"Column {column} = {np.mean(data[:, column])}")
    if np.mean(data[:, column]) > 0.5:   # 1
        gamma += '1'
        epsilon += '0'
    else:
        gamma += '0'
        epsilon += '1'

print(f"{gamma=}, {epsilon=}")

gamma = int(gamma, 2)
epsilon = int(epsilon, 2)

print(f"{gamma=}, {epsilon=}, {gamma*epsilon=}")

candidates = np.array(range(rows), dtype=np.uint32)
column = 0
while len(candidates) > 1:
    if np.mean(data[candidates, column]) >= 0.5:
        candidates = candidates[np.flatnonzero(data[candidates, column] == 1)]
    else:
        candidates = candidates[np.flatnonzero(data[candidates, column] == 0)]
    column += 1

oxygen = data[candidates[0], :]

candidates = np.array(range(rows), dtype=np.uint32)
column = 0
while len(candidates) > 1:
    if np.mean(data[candidates, column]) >= 0.5:
        candidates = candidates[np.flatnonzero(data[candidates, column] == 0)]
    else:
        candidates = candidates[np.flatnonzero(data[candidates, column] == 1)]
    column += 1

carbon_dioxide = data[candidates[0], :]

print(f"{oxygen=}, {carbon_dioxide=}")

oxygen = int(''.join(map(str, oxygen)), 2)
carbon_dioxide = int(''.join(map(str, carbon_dioxide)), 2)

print(f"{oxygen=}, {carbon_dioxide=}, {oxygen*carbon_dioxide=}")

pass
