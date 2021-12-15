#! /usr/bin/env python3

from collections import namedtuple, Counter
from pathlib import Path

import numpy as np

with Path("../inputs/05.txt").open("r") as handle:
    lines = list([line.strip() for line in handle.readlines()])

lines = list(map(lambda l: l.replace(" -> ", ",").split(","), lines))
lines = list(map(lambda l: list(map(int, l)), lines))

Line = namedtuple("Line", ["x1", "y1", "x2", "y2"])

lines = list([Line(*line) for line in lines])

x_values = set(map(lambda l: l.x1, lines))
x_values.update(map(lambda l: l.x2, lines))
y_values = set(map(lambda l: l.y1, lines))
y_values.update(map(lambda l: l.y2, lines))
max_x = max(x_values)
max_y = max(y_values)

plane = np.zeros((max_y+1, max_x+1), dtype=np.uint32)

for line in lines:
    if line.y2 == line.y1:    # horizontal
        for x in range(min(line.x1, line.x2), max(line.x1, line.x2) + 1):
            plane[line.y1, x] += 1
    elif line.x2 == line.x1:
        for y in range(min(line.y1, line.y2), max(line.y1, line.y2) + 1):
            plane[y, line.x1] += 1
    else:
        pass    # print(f"Skipping {line} - neither horizontal nor vertical.")

danger = np.count_nonzero(plane >= 2)
print(f"{danger=}")

for line in lines:
    if (line.x2 != line.x1) and (line.y2 != line.y1):   # diagonal
        assert abs(line.x2-line.x1) == abs(line.y2-line.y1), f"{line} is not diagonal!"
        delta_x = line.x2 - line.x1
        delta_x = delta_x // abs(delta_x)
        delta_y = line.y2 - line.y1
        delta_y = delta_y // abs(delta_y)
        x, y = line.x1, line.y1
        while x != (line.x2 + delta_x):
            plane[y, x] += 1
            x += delta_x
            y += delta_y

danger = np.count_nonzero(plane >= 2)
print(f"{danger=}")

pass
