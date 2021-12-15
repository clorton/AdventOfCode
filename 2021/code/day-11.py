#! /usr/bin/env python3

from pathlib import Path

import numpy as np

with Path("../inputs/11.txt").open("r") as handle:
    lines = list([list(map(int, line.strip())) for line in handle.readlines()])

# lines = [list(map(int, line)) for line in [
#     "5483143223",
#     "2745854711",
#     "5264556173",
#     "6141336146",
#     "6357385478",
#     "4167524645",
#     "2176841721",
#     "6882881134",
#     "4846848554",
#     "5283751526",
# ]]

lines = np.array(lines, dtype=np.int32)
octopi = np.zeros((12, 12), dtype=np.int32)
octopi[1:11, 1:11] = lines

total = 0
num_steps = 100
for step in range(num_steps):
    flashed = np.full_like(octopi, False, dtype=bool)
    octopi[1:11, 1:11] += 1
    flash = octopi[1:11, 1:11] > 9
    while np.any(flash):
        flashes = np.nonzero(flash)
        for y, x in zip(*flashes):
            flashed[y+1, x+1] = True
            octopi[y, x] += 1
            octopi[y, x+1] += 1
            octopi[y, x+2] += 1
            octopi[y+1, x] += 1
            octopi[y+1, x+1] = 0
            octopi[y+1, x+2] += 1
            octopi[y + 2, x] += 1
            octopi[y + 2, x+1] += 1
            octopi[y + 2, x+2] += 1
        flash = octopi[1:11, 1:11] > 9
    octopi[flashed.nonzero()] = 0
    total += np.count_nonzero(flashed)

print(f"{total=} after {num_steps} steps")

# Part 2

octopi[1:11, 1:11] = lines

count = 0
step = 0
while count != 100:
    flashed = np.full_like(octopi, False, dtype=bool)
    octopi[1:11, 1:11] += 1
    flash = octopi[1:11, 1:11] > 9
    while np.any(flash):
        flashes = np.nonzero(flash)
        for y, x in zip(*flashes):
            flashed[y+1, x+1] = True
            octopi[y, x] += 1
            octopi[y, x+1] += 1
            octopi[y, x+2] += 1
            octopi[y+1, x] += 1
            octopi[y+1, x+1] = 0
            octopi[y+1, x+2] += 1
            octopi[y + 2, x] += 1
            octopi[y + 2, x+1] += 1
            octopi[y + 2, x+2] += 1
        flash = octopi[1:11, 1:11] > 9
    octopi[flashed.nonzero()] = 0
    step += 1
    count = np.count_nonzero(flashed)

print(f"100 simultaneous flashes after {step} steps")

pass
