from pathlib import Path

import numpy as np

with (Path(__file__).parent / "day-10.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# Begin at 0, end at 9 only move L/R/U/D, and only increase in height by 1.
# Score = # of 9-height positions reachable from the trailhead.

# Score = 36

# lines = [
#     "89010123",
#     "78121874",
#     "87430965",
#     "96549874",
#     "45678903",
#     "32019012",
#     "01329801",
#     "10456732",
# ]

topo = np.array([list(map(int, list(line))) for line in lines])

from collections import namedtuple

Pos = namedtuple("Pos", ["y", "x"])

trailheads = [Pos(*entry) for entry in zip(*np.nonzero(topo == 0))]

def test(x, y, topo):
    check = topo[y, x] + 1
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        xp, yp = x + dx, y + dy
        if (0 <= xp) and (xp < topo.shape[1]) and (0 <= yp) and (yp < topo.shape[0]):
            if topo[yp, xp] == check:
                yield Pos(yp, xp)
    return

scores = {}
for trailhead in trailheads:
    scores[trailhead] = set()
    pos = [trailhead]
    while pos:
        y, x = pos.pop(0)
        height = topo[y,x]
        for okay in test(x, y, topo):
            if topo[okay.y, okay.x] == 9:
                scores[trailhead].add(okay)
            else:
                pos.append(okay)

total = 0
for key, peaks in scores.items():
    total += len(peaks)

print(f"Total = {total}")

scores = {}
for trailhead in trailheads:
    scores[trailhead] = 0
    pos = [trailhead]
    while pos:
        y, x = pos.pop(0)
        height = topo[y,x]
        for okay in test(x, y, topo):
            if topo[okay.y, okay.x] == 9:
                scores[trailhead] += 1
            else:
                pos.append(okay)

total = 0
for key, score in scores.items():
    total += score

print(f"Total = {total}")

print("Done.")
