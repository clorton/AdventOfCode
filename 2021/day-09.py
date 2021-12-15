#! /usr/bin/env python3

from functools import reduce
from operator import mul
from pathlib import Path

import numpy as np
from scipy import ndimage

with Path("09.txt").open("r") as handle:
    lines = list([line.strip() for line in handle.readlines()])

lines = list([list(map(int, list(line))) for line in lines])

heightmap = np.array(lines, dtype=np.uint32)

"""
heightmap = np.array([
    [2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
    [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
    [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
    [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
    [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]
], dtype=np.uint32)
"""

compare = np.full(heightmap.shape, 1000000, dtype=np.int32)
compare[0:-1, :] = heightmap[1:, :]   # compare to next row
lower = heightmap < compare
compare.fill(1000000)
compare[1:, :] = heightmap[0:-1, :]   # compare to previous column
lower &= heightmap < compare
compare.fill(1000000)
compare[:, 0:-1] = heightmap[:, 1:]   # compare to next row
lower &= heightmap < compare
compare.fill(1000000)
compare[:, 1:] = heightmap[:, 0:-1]   # compare to previous row
lower &= heightmap < compare

risk = heightmap[lower.nonzero()]
risk += 1
risk = np.sum(risk)
print(f"{risk=}")   # ¡465!

# Part 2

mask = heightmap < 9
labels, nb = ndimage.label(mask)

sizes = [np.count_nonzero(labels == label) for label in range(1, nb+1)]
sizes = sorted(sizes)
largest = sizes[-3:]
product = reduce(mul, largest, 1)
print(f"{largest} => {product=}")

pass
