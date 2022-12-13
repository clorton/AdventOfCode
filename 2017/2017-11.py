#! /usr/bin/env python3

from pathlib import Path
WORK_DIR = Path(__file__).parent.absolute()

with (WORK_DIR / "2017-11.txt").open("r") as handle:
    steps = handle.readline().strip().split(',')

# Use a checkerboard layout to model the hexagonal grid.

deltas = {
    'n': (0, 2),
    'ne': (1, 1),
    'se': (1, -1),
    's': (0, -2),
    'sw': (-1, -1),
    'nw': (-1, 1)
}


x = 0
y = 0
dist = 0
max_dist = 0
for step in steps:
    dx, dy = deltas[step]
    x += dx
    y += dy
    # print('x = {0}, y = {1}'.format(x, y))
    dist = int(abs(x) / 2.0 + abs(y) / 2.0)
    max_dist = max(dist, max_dist)

print(f"Part 1: current distance = {dist}")
print(f"Part 2: maximum distance = {max_dist}")
