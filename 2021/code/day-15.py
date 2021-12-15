#! /usr/bin/env python3

from collections import Counter, defaultdict, namedtuple
from datetime import datetime
from heapq import heappush, heappop
from pathlib import Path

import numpy as np

t_start = datetime.now()

with Path("../inputs/15.txt").open("r") as handle:
    lines = list([list(map(int, list(line.strip()))) for line in handle.readlines()])

"""
lines = [
    list(map(int, list("1163751742"))),
    list(map(int, list("1381373672"))),
    list(map(int, list("2136511328"))),
    list(map(int, list("3694931569"))),
    list(map(int, list("7463417111"))),
    list(map(int, list("1319128137"))),
    list(map(int, list("1359912421"))),
    list(map(int, list("3125421639"))),
    list(map(int, list("1293138521"))),
    list(map(int, list("2311944581")))
]
"""

inputs = np.array(lines, dtype=np.int32)
height, width = inputs.shape
risk = np.full((height + 2, width + 2), 1_000_000, dtype=np.int32)
risk[1:height + 1, 1:width + 1] = inputs

Move = namedtuple("Move", ["dy", "dx"])
Position = namedtuple("Position", ["x", "y"])
Path = namedtuple("Path", ["cost", "steps"])

moves = [Move(0, 1), Move(1, 0), Move(0, -1), Move(-1, 0)]


def find_path(risks):
    start = Position(1, 1)
    target_y, target_x = risks.shape
    target_x -= 2
    target_y -= 2
    target = Position(target_x, target_y)
    paths = []
    heappush(paths, Path(0, [start]))
    bests = np.full_like(risks, 1_000_000)
    iterations = 0
    while True:
        iterations += 1
        # if (count % 100) == 0:
        #     print(f"{count=}")
        if len(paths) == 0:
            raise RuntimeError
        path = heappop(paths)
        if path.steps[-1] == target:
            min_risk = path
            break
        x, y = path.steps[-1]
        for move in moves:
            new_x = x + move.dx
            new_y = y + move.dy
            cost = path.cost + risks[new_y, new_x]
            if cost < bests[new_y][new_x]:
                position = Position(new_x, new_y)
                steps = list(path.steps)
                steps.append(position)
                new_path = Path(cost, steps)
                bests[new_y][new_x] = cost
                heappush(paths, new_path)

    return min_risk, iterations

t_prep_part1 = datetime.now()

minimum_risk, count = find_path(risk)
print(f"{minimum_risk.cost=} ({count=})")

t_calc_part1 = datetime.now()

big_risk = np.full((5*height+2, 5*width+2), 1_000_000, dtype=np.int32)
big_risk[1:height+1, 1:width+1] = inputs
for row in range(5):
    for column in range(5):
        if row != 0 or column != 0:
            big_risk[row*height+1:(row+1)*height+1, column*width+1:(column+1)*width+1] = ((inputs + row + column - 1) % 9) + 1

t_prep_part2 = datetime.now()

minimum_risk, count = find_path(big_risk)
print(f"{minimum_risk.cost=}")

t_calc_part2 = datetime.now()

print(f"{t_prep_part1-t_start=}")
print(f"{t_calc_part1-t_prep_part1=}")
print(f"{t_prep_part2-t_calc_part1=}")
print(f"{t_calc_part2-t_prep_part2=}")

pass
