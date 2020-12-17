#! /usr/bin/env python3

import numpy as np
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-17.txt").read_text()
lines = text.split("\n")
start = [list(map(lambda x: 1 if x == "#" else 0, line)) for line in lines]

# part 1
width = len(start[0])
cycles = 6
offset = cycles + 1
dimension = width + (offset*2)
pocket = np.zeros((dimension, dimension, dimension), dtype=np.uint8)
pocket[dimension//2, offset:offset+width, offset:offset+width] = start

for cycle in range(cycles):
    tplusone = np.zeros_like(pocket)
    for z in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for x in [-1, 0, 1]:
                if x != 0 or y != 0 or z != 0:
                    tplusone[1:dimension-1, 1:dimension-1, 1:dimension-1] += pocket[1+z:dimension-1+z, 1+y:dimension-1+y, 1+x:dimension-1+x]

    active = (pocket[:, :, :] == 1) * ((tplusone[:, :, :]) == 2 + (tplusone[:, :, :] == 3))
    active += (pocket[:, :, :] == 0) * (tplusone[:, :, :] == 3)
    pocket = np.zeros_like(pocket, dtype=np.uint8)
    pocket[active] += 1

live = np.sum(pocket)
print(f"{live} active cells after {cycles} cycles")

# part 2
pocket = np.zeros((dimension, dimension, dimension, dimension), dtype=np.uint8)
pocket[dimension//2, dimension//2, offset:offset+width, offset:offset+width] = start

for cycle in range(cycles):
    tplusone = np.zeros_like(pocket)
    for w in [-1, 0, 1]:
        for z in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for x in [-1, 0, 1]:
                    if x != 0 or y != 0 or z != 0 or w != 0:
                        tplusone[1:dimension-1, 1:dimension-1, 1:dimension-1, 1:dimension-1] += pocket[1+w:dimension-1+w, 1+z:dimension-1+z, 1+y:dimension-1+y, 1+x:dimension-1+x]

    active = (pocket[:, :, :, :] == 1) * ((tplusone[:, :, :, :]) == 2 + (tplusone[:, :, :, :] == 3))
    active += (pocket[:, :, :, :] == 0) * (tplusone[:, :, :, :] == 3)
    pocket = np.zeros_like(pocket, dtype=np.uint8)
    pocket[active] += 1

live = np.sum(pocket)
print(f"{live} active cells after {cycles} cycles")

print(".oO( done )")
