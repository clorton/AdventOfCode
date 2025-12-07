from collections import namedtuple
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

with Path(HERE / "day-07.txt").open("rt") as file:
    lines = [list(map(ord, line.strip("\n"))) for line in file.readlines()]

SPACE = ord(".")
SPLIT = ord("^")

manifold = np.array(lines, dtype=np.uint8)

start = np.nonzero(manifold == ord("S"))
Beam = namedtuple("Beam", ["row", "col"])
beams = {Beam(start[0][0], start[1][0])}
splits = 0

while beams:
    updated = set()
    for (row, col) in beams:
        row += 1
        if row < manifold.shape[0]:
            if manifold[row,col] == SPLIT:
                updated.update([Beam(row,col-1), Beam(row,col+1)])
                splits += 1
            else:
                updated.add(Beam(row,col))
    beams = updated

print(f"Part I:  {splits=}")

##### Part II #####

"""
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............

.......S.......
.......1.......
......1^1......
......1.1......
.....1^2^1.....
.....1.2.1.....
....1^3^3^1....
....1.3.3.1....
...1^4^331^1...
...1.4.331.1...
..1^5^434^2^1..
..1.5.434.2.1..
.1^154^74.21^1.
.1.154.74.21.1.
1^2^A^B^B^211^1
1.2.A.B.B.211.1

1 + 2 + 10 + 11 + 11 + 2 + 1 + 1 + 1 = 40
"""

test = False
if test:
    manifold = [
        ".......S.......",
        "...............",
        ".......^.......",
        "...............",
        "......^.^......",
        "...............",
        ".....^.^.^.....",
        "...............",
        "....^.^...^....",
        "...............",
        "...^.^...^.^...",
        "...............",
        "..^...^.....^..",
        "...............",
        ".^.^.^.^.^...^.",
        "...............",
    ]
    manifold = np.array([list(map(ord, line)) for line in manifold], dtype=np.uint8)
    start = np.nonzero(manifold == ord("S"))

counts = np.zeros_like(manifold, dtype=np.int64)
counts[start[0][0],start[1][0]] = 1

for row in range(counts.shape[0]-1):
    for col in range(counts.shape[1]):
        if (count := counts[row,col]) != 0:
            rnext = row + 1
            if manifold[rnext,col] == SPLIT:
                counts[rnext,col-1] += count
                counts[rnext,col+1] += count
            else:
                counts[rnext,col] += count

paths = counts[-1].sum()

print(f"Part II: {paths=}")

print("done")
