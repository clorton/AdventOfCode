#! /usr/bin/env python3

from collections import defaultdict, namedtuple
from fractions import Fraction
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
# filename, (minx, miny, maxx, maxy) = "example.txt", (7, 7, 27, 27)
filename, (minx, miny, maxx, maxy) = "input.txt", (200_000_000_000_000, 200_000_000_000_000, 400_000_000_000_000, 400_000_000_000_000)
INPUT_FILE = Path(__file__).parent / filename

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

Stone = namedtuple("Stone", ["x", "y", "z", "dx", "dy", "dz"])

data = []
for line in input:
    position, velocity = line.split(" @ ")
    position = list(map(int, position.split(", ")))
    velocity = list(map(int, velocity.split(", ")))
    data.append(Stone(*(position+velocity)))

inbounds = 0
for ia in tqdm(range(len(data)-1)):
    a = data[ia]
    # ax = a.x + t*a.dx
    # ay = a.y + t*a.dy
    # ta = (ay - a.y) / a.dy
    # ax = a.x + (ay - a.y) * a.dx / a.dy

    for ib in range(ia+1, len(data)):
        b = data[ib]

        # bx = b.x + t*b.dx
        # by = b.y + t*b.dy
        # tb = (by - b.y) / b.dy
        # bx = b.x + (by - b.y) * b.dx / b.dy

        # a.x + (y - a.y) * a.dx / a.dy = b.x + (y - b.y) * b.dx / b.dy
        # a.x + y * a.dx / a.dy - a.y * a.dx / a.dy = b.x + y * b.dx / b.dy - b.y * b.dx / b.dy
        # y * ((a.dx / a.dy) - (b.dx / b.dy)) = b.x - a.x + (a.y * a.dx / a.dy) - (b.y * b.dx / b.dy)
        # y = (b.x - a.x + (a.y * a.dx / a.dy) - (b.y * b.dx / b.dy)) / ((a.dx / a.dy) - (b.dx / b.dy))
        denominator = Fraction(a.dx, a.dy) - Fraction(b.dx, b.dy)

        if denominator == 0:
            # parallel
            continue

        y = (b.x - a.x + Fraction(a.y * a.dx, a.dy) - Fraction(b.y * b.dx, b.dy)) / denominator
        x = a.x + (y - a.y) * Fraction(a.dx, a.dy)
        ta = Fraction((x - a.x), a.dx)
        tb = Fraction((x - b.x), b.dx)
        
        if (ta < 0) or (tb < 0):
            # collision is in the past
            continue

        if (minx <= x <= maxx) and (miny <= y <= maxy):
            # print(f"Collision between {ia} and {ib} at ({x}, {y}) at time {ta} ({tb})")
            inbounds += 1
        
        # out of bounds
        ...

print(f"Number of collisions in bounds: {inbounds}")

for ia in tqdm(range(len(data)-1)):
    a = data[ia]
    ax = a.x + ta*a.dx
    ay = a.y + ta*a.dy
    az = a.z + ta*a.dz

    for ib in range(ia+1, len(data)):
        b = data[ib]
        bx = b.x + tb*b.dx
        by = b.y + tb*b.dy
        bz = b.z + tb*b.dz

        for ic in range(ib+1, len(data)):
            c = data[ic]
            cx = c.x + tc*c.dx
            cy = c.y + tc*c.dy
            cz = c.z + tc*c.dz

pass
