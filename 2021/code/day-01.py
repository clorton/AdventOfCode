#! /usr/bin/env python3

from pathlib import Path
import numpy as np

with Path("../inputs/01.txt").open("r") as handle:
    data = handle.readlines()

data = np.array(list(map(lambda n: int(n), data)), dtype=np.int64)
deltas = data[1:] - data[0:-1]
increasing = np.count_nonzero(deltas > 0)
print(f"Day 1, Part 1: {increasing} increasing readings")

windows = data[0:-2] + data[1:-1] + data[2:]
deltas = windows[1:] - windows[0:-1]
increasing = np.count_nonzero(deltas > 0)
print(f"Day 2, Part 2: {increasing} increasing readings")

pass
